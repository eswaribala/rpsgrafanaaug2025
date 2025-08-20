from flask import Flask
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Set up metrics
resource = Resource(attributes={
    SERVICE_NAME: "sample-flask-app"
})

exporter = OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")  # Point to OTEL Collector
reader = PeriodicExportingMetricReader(exporter)

provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Create a simple counter
counter = meter.create_counter(
    name="sample_requests_total",
    description="Number of requests",
    unit="1",
)

app = Flask(__name__)

@app.route("/")
def hello():
    counter.add(1, {"route": "/"})
    return "Hello, OpenTelemetry!"

if __name__ == "__main__":
    app.run(port=5000)
