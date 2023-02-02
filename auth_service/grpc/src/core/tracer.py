import inspect
from contextlib import nullcontext
from functools import wraps
from typing import Callable, Iterator, Any

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.grpc import aio_server_interceptor
from opentelemetry.instrumentation.grpc._aio_server import OpenTelemetryAioServerInterceptor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, DEPLOYMENT_ENVIRONMENT
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.trace import set_tracer_provider, NonRecordingSpan
from opentelemetry.util.types import AttributeValue

from core.config import get_settings


def setup_tracer() -> OpenTelemetryAioServerInterceptor:
    provider = TracerProvider(
        sampler=TraceIdRatioBased(1.0),
        resource=Resource.create(
            {
                DEPLOYMENT_ENVIRONMENT: "production",
                SERVICE_NAME: get_settings().jaeger.service_name,
            }
        ),
        shutdown_on_exit=True,
    )
    span_processor = BatchSpanProcessor(
        JaegerExporter(
            agent_host_name=get_settings().jaeger.host,
            agent_port=get_settings().jaeger.port,
        )
    )

    set_tracer_provider(provider)
    provider.add_span_processor(span_processor)
    return aio_server_interceptor(tracer_provider=provider)


class Instrumented:
    def __init__(self, span_name: str = None, span_attributes: dict[str, AttributeValue] | None = None, **kwargs):
        self.span_name = span_name
        self.span_attributes = span_attributes
        self.kwargs = kwargs

    @staticmethod
    def get_span(
        module_name: str, span_name: str, span_attributes: dict[str, AttributeValue] | None, **kwargs
    ) -> Iterator[Span | None]:
        if isinstance(trace.get_current_span(), NonRecordingSpan):
            span = nullcontext()
        else:
            span_attributes = span_attributes if span_attributes is not None else {}
            span = trace.get_tracer(module_name).start_as_current_span(span_name, attributes=span_attributes, **kwargs)

        return span

    def __call__(self, wrapped_function: Callable) -> Callable:
        module = inspect.getmodule(wrapped_function)
        is_async = inspect.iscoroutinefunction(wrapped_function)
        module_name = __name__

        if module is not None:
            module_name = module.__name__

        span_name = self.span_name or wrapped_function.__qualname__

        @wraps(wrapped_function)
        def new_f(*args, **kwargs):
            with self.get_span(
                module_name=module_name, span_name=span_name, span_attributes=self.span_attributes, **self.kwargs
            ):
                return wrapped_function(*args, **kwargs)

        @wraps(wrapped_function)
        async def new_f_async(*args, **kwargs):
            with self.get_span(
                module_name=module_name, span_name=span_name, span_attributes=self.span_attributes, **self.kwargs
            ):
                return await wrapped_function(*args, **kwargs)

        return new_f_async if is_async else new_f


def instrumented(
    wrapped_function: Callable[[Any], Any] | None = None,
    *,
    span_name: str | None = None,
    span_attributes: dict[str, AttributeValue] | None = None,
    **kwargs
):
    """
    Decorator to enable opentelemetry instrumentation on a function.
    When the decorator is used, a child span will be created in the current trace
    context, using the fully-qualified function name as the span name.

    Alternatively, the span name can be set manually by setting the span_name parameter
        @param wrapped_function:  function or method to wrap
        @param span_name:  optional span name.  Defaults to fully qualified function name of wrapped function
        @param span_attributes: optional dictionary of attributes to be set on the span
    """
    inst = Instrumented(span_name=span_name, span_attributes=span_attributes, **kwargs)

    if wrapped_function:
        return inst(wrapped_function)

    return inst
