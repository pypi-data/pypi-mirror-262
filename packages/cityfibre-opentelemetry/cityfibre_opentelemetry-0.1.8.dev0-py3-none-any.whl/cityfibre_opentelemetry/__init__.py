import logging
from os import environ

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from cityfibre_opentelemetry.environment_variables import (
    OTEL_SERVICE_NAME,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_EXPORTER_OTLP_TRACES_HEADERS,
    OTEL_EXPORTER_OTLP_LOGS_ENDPOINT,
    OTEL_EXPORTER_OTLP_LOGS_HEADERS
)

resource = Resource.create(
    {
        "service.name": environ.get(OTEL_SERVICE_NAME),
        "service.instance.id": environ.get(OTEL_SERVICE_NAME)
    }
)

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)
span_exporter = OTLPSpanExporter(
    endpoint=environ.get(OTEL_EXPORTER_OTLP_TRACES_ENDPOINT),
    headers=environ.get(OTEL_EXPORTER_OTLP_TRACES_HEADERS)
)
tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
logs_exporter = OTLPLogExporter(
    endpoint=environ.get(OTEL_EXPORTER_OTLP_LOGS_ENDPOINT),
    headers=environ.get(OTEL_EXPORTER_OTLP_LOGS_HEADERS)
)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(logs_exporter))
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
tracer = trace.get_tracer(__name__)


def get_context(msk_event_headers):
    carrier = {}
    for header in msk_event_headers:
        for key in header:
            carrier[key] = bytes(header[key]).decode()

    return TraceContextTextMapPropagator().extract(carrier=carrier)


def produce_hook(span, args, kwargs):
    if span and span.is_recording():
        topic = args[0]
        span.set_attribute("messaging.system", f"kafka-{topic}")


KafkaInstrumentor().instrument(produce_hook=produce_hook)
RequestsInstrumentor().instrument()
