"""Integration for instrumenting Pydantic models."""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING, Any, ClassVar, Literal, TypedDict

from opentelemetry.metrics import Counter
from pydantic_core import CoreConfig, CoreSchema

import logfire
from logfire import LogfireSpan
from logfire._config import GLOBAL_CONFIG

if TYPE_CHECKING:
    from pydantic import ValidationError
    from pydantic.plugin import (
        SchemaKind,
        SchemaTypePath,
        ValidateJsonHandlerProtocol,
        ValidatePythonHandlerProtocol,
        ValidateStringsHandlerProtocol,
    )
    from typing_extensions import TypeAlias

    # It might make sense to export the following type alias from `pydantic.plugin`, rather than redefining it here.
    StringInput: TypeAlias = 'dict[str, StringInput]'

METER = GLOBAL_CONFIG._meter_provider.get_meter('pydantic-plugin-meter')  # type: ignore


class PluginSettings(TypedDict, total=False):
    """A typed dict for the Pydantic plugin settings.

    This is how you can use the [`PluginSettings`][logfire.integrations.pydantic_plugin.PluginSettings]
    with a Pydantic model:

    ```py
    from logfire.integrations.pydantic_plugin import PluginSettings
    from pydantic import BaseModel


    class Model(BaseModel, plugin_settings=PluginSettings(logfire={'record': 'all'})):
        a: int
    ```
    """

    logfire: LogfireSettings
    """Settings for the logfire integration."""


class LogfireSettings(TypedDict, total=False):
    """Settings for the logfire integration."""

    trace_sample_rate: float
    """The sample rate to use for tracing."""
    tags: list[str]
    """Tags to add to the spans."""
    record: Literal['all', 'failure', 'metrics']
    """What to record.

    The following values are supported:

    * `all`: Record all validation events.
    * `failure`: Record only validation failures.
    * `metrics`: Record only validation metrics.
    """


_USER_STACK_OFFSET = 3
"""The number of frames to skip when logging from user code."""


class BaseValidateHandler:
    """Base class for validation event handler classes."""

    validation_method: ClassVar[str]
    span: LogfireSpan | None
    __slots__ = (
        'schema_name',
        'span',
        '_record',
        '_successful_validation_counter',
        '_failed_validation_counter',
        '_logfire',
    )

    def __init__(
        self,
        schema: CoreSchema,
        _config: CoreConfig | None,
        _plugin_settings: PluginSettings | dict[str, Any],
        schema_type_path: SchemaTypePath,
        record: Literal['all', 'failure', 'metrics'],
    ) -> None:
        # We accept the schema, config, and plugin_settings in the init since these are the things
        # that are currently exposed by the plugin to potentially configure the validation handlers.
        self.schema_name = get_schema_name(schema)
        self._record = record

        model_name = schema_type_path.name.split('.')[-1]
        # There are characters not allowed, we need to replace them, see:
        # https://github.com/open-telemetry/opentelemetry-python/blob/18c0cb4c0de9af5ab9783d6c7770e57b448c3bf2/opentelemetry-api/src/opentelemetry/metrics/_internal/instrument.py#L41
        model_name = re.sub(r'[^-_./a-zA-Z0-9]', '_', model_name)
        # Must start with a letter
        model_name = re.sub(r'^[^a-zA-Z]+', '', model_name)
        # Remove repeated underscores
        model_name = re.sub(r'_+', '_', model_name)
        # As the counter name should be less than 63 chars, we only get the last 40 chars of model name
        model_name = model_name[-40:]
        self._successful_validation_counter = _create_counter(name=f'{model_name}-successful-validation')
        self._failed_validation_counter = _create_counter(name=f'{model_name}-failed-validation')

        self._logfire = logfire.DEFAULT_LOGFIRE_INSTANCE
        # trace_sample_rate = _plugin_settings.get('logfire', {}).get('trace_sample_rate')
        # if trace_sample_rate:
        #     self._logfire = self._logfire.with_trace_sample_rate(float(trace_sample_rate))

        tags = _plugin_settings.get('logfire', {}).get('tags')
        if tags:
            if isinstance(tags, str):
                tags = [tags]
            self._logfire = self._logfire.with_tags(*tags)

        self.span = None

    def _on_enter(
        self,
        input_data: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
        self_instance: Any | None = None,
    ) -> None:
        if self._record == 'all':
            self.span = self._logfire.span(
                'Pydantic {schema_name} {validation_method}',
                schema_name=self.schema_name,
                validation_method=self.validation_method,
                input_data=input_data,
                _span_name=f'pydantic.{self.validation_method}',
            ).__enter__()

    def on_success(self, result: Any) -> None:
        """Callback to be notified of successful validation.

        Args:
            result: The result of the validation.
        """
        if self._record == 'all':
            self._logfire.log(
                'debug',
                msg_template='Validation successful {result=!r}',
                attributes={'result': result},
                stack_offset=_USER_STACK_OFFSET,
            )

        self._successful_validation_counter.add(1)

        if self.span:
            self.span.__exit__(None, None, None)

    def on_error(self, error: ValidationError) -> None:
        """Callback to be notified of validation errors.

        Args:
            error: The validation error.
        """
        error_count = error.error_count()
        self._logfire.log(
            level='warn',
            msg_template='Validation on {schema_name} failed',
            attributes={
                'schema_name': self.schema_name,
                'error_count': error_count,
                'errors': error.errors(include_url=False),
            },
            stack_offset=_USER_STACK_OFFSET,
        )
        self._failed_validation_counter.add(1)
        if self.span:
            self.span.__exit__(None, None, None)

    def on_exception(self, exception: Exception) -> None:
        """Callback to be notified of validation exceptions.

        Args:
            exception: The exception raised during validation.
        """
        self._logfire.log(
            'error',
            msg_template='{exception_type=}: {exception_msg=}',
            attributes={'exception': type(exception).__name__, 'exception_msg': exception},
            stack_offset=_USER_STACK_OFFSET,
        )
        if self.span:
            self.span.__exit__(type(exception), exception, exception.__traceback__)


def get_schema_name(schema: CoreSchema) -> str:
    """Find the best name to use for a schema.

    The follow rules are used:
    * If the schema represents a model or dataclass, use the name of the class.
    * If the root schema is a wrap/before/after validator, look at its `schema` property.
    * Otherwise use the schema's `type` property.

    Args:
        schema: The schema to get the name for.

    Returns:
        The name of the schema.
    """
    schema_type = schema['type']
    if schema_type in {'model', 'dataclass'}:
        return schema['cls'].__name__  # type: ignore
    elif schema_type in {'function-after', 'function-before', 'function-wrap'}:
        return get_schema_name(schema['schema'])  # type: ignore
    else:
        return schema_type


@lru_cache
def _create_counter(name: str) -> Counter:
    return METER.create_counter(name=name)


class ValidatePythonHandler(BaseValidateHandler):
    """Implements `pydantic.plugin.ValidatePythonHandlerProtocol`."""

    validation_method = 'validate_python'

    def on_enter(  # noqa: D102
        self,
        input: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
        self_instance: Any | None = None,
    ) -> None:
        self._on_enter(
            input, strict=strict, from_attributes=from_attributes, context=context, self_instance=self_instance
        )


class ValidateJsonHandler(BaseValidateHandler):
    """Implements `pydantic.plugin.ValidateJsonHandlerProtocol`."""

    validation_method = 'validate_json'

    def on_enter(  # noqa: D102
        self,
        input: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        context: dict[str, Any] | None = None,
        self_instance: Any | None = None,
    ) -> None:
        self._on_enter(input, strict=strict, context=context, self_instance=self_instance)


class ValidateStringsHandler(BaseValidateHandler):
    """Implements `pydantic.plugin.ValidateStringsHandlerProtocol`."""

    validation_method = 'validate_strings'

    def on_enter(  # noqa: D102
        self, input: StringInput, *, strict: bool | None = None, context: dict[str, Any] | None = None
    ) -> None:
        self._on_enter(input, strict=strict, context=context)


@dataclass
class LogfirePydanticPlugin:
    """Implements `pydantic.plugin.PydanticPluginProtocol`.

    Set the `LOGFIRE_DISABLE_PYDANTIC_PLUGIN` environment variable to `true` to disable the plugin.

    Note:
        In the future, you'll be able to use the `PYDANTIC_DISABLE_PLUGINS` instead.

        See [pydantic/pydantic#7709](https://github.com/pydantic/pydantic/issues/7709) for more information.
    """

    def new_schema_validator(
        self,
        schema: CoreSchema,
        schema_type: Any,
        schema_type_path: SchemaTypePath,
        schema_kind: SchemaKind,
        config: CoreConfig | None,
        plugin_settings: dict[str, Any],
    ) -> tuple[
        ValidatePythonHandlerProtocol | None, ValidateJsonHandlerProtocol | None, ValidateStringsHandlerProtocol | None
    ]:
        """This method is called every time a new `SchemaValidator` is created.

        Args:
            schema: The schema to validate against.
            schema_type: The original type which the schema was created from, e.g. the model class.
            schema_type_path: Path defining where `schema_type` was defined, or where `TypeAdapter` was called.
            schema_kind: The kind of schema to validate against.
            config: The config to use for validation.
            plugin_settings: The plugin settings.

        Returns:
            A tuple of event handlers for each of the three validation methods -
                `validate_python`, `validate_json`, `validate_strings` or a tuple of
                three `None` if recording is `off`.
        """
        record = 'off'

        logfire_settings = plugin_settings.get('logfire')
        if logfire_settings and 'record' in logfire_settings:
            record = logfire_settings['record']
        else:
            record = GLOBAL_CONFIG.pydantic_plugin.record

        if record == 'off':
            return None, None, None

        if _include_model(schema, schema_type_path):
            return (
                ValidatePythonHandler(schema, config, plugin_settings, schema_type_path, record),
                ValidateJsonHandler(schema, config, plugin_settings, schema_type_path, record),
                ValidateStringsHandler(schema, config, plugin_settings, schema_type_path, record),
            )

        return None, None, None


plugin = LogfirePydanticPlugin()

# set of modules to ignore completed
IGNORED_MODULE_PREFIXES: tuple[str, ...] = 'fastapi.', 'logfire_backend.'


def _include_model(schema: CoreSchema, schema_type_path: SchemaTypePath) -> bool:
    """Check whether a model should be instrumented."""
    include = GLOBAL_CONFIG.pydantic_plugin.include
    exclude = GLOBAL_CONFIG.pydantic_plugin.exclude

    schema_type = schema['type']
    if schema_type in {'function-after', 'function-before', 'function-wrap'}:
        return _include_model(schema['schema'])  # type: ignore

    # check if the model is in ignored model
    if any(schema_type_path.module.startswith(prefix) for prefix in IGNORED_MODULE_PREFIXES):
        return False

    # check if the model is in exclude models
    if exclude and any(
        re.search(f'{pattern}$', f'{schema_type_path.module}::{schema_type_path.name}') for pattern in exclude
    ):
        return False

    # check if the model is in include models
    if include:
        return any(
            re.search(f'{pattern}$', f'{schema_type_path.module}::{schema_type_path.name}') for pattern in include
        )
    return True


if TYPE_CHECKING:
    # This is just to ensure we get type checking that the plugin actually implements the expected protocol.
    from pydantic.plugin import PydanticPluginProtocol

    def check_plugin_protocol(_plugin: PydanticPluginProtocol) -> None:  # noqa: D103
        pass

    check_plugin_protocol(plugin)
