import functools

from flask import request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .config import settings

resource = Resource(attributes={
    SERVICE_NAME: "Auth_sprint_2"
})

jaeger_exporter = JaegerExporter(
    agent_host_name=settings.JAEGER_HOST_NAME,
    agent_port=settings.JAEGER_UDP,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)


tracer = trace.get_tracer(__name__)


def tracing(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        request_id = request.headers.get('X-Request-Id')
        with tracer.start_span(name=fn.__name__) as span:
            span.set_attribute('http.request_id', request_id)
            return fn(*args, **kwargs)
    return decorated
