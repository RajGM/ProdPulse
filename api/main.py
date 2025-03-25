from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
from starlette.responses import JSONResponse

import asyncio
from contextlib import asynccontextmanager
from metrics.collector import collect_metrics, cpu_usage_gauge, memory_usage_gauge, disk_usage_gauge
from prometheus_fastapi_instrumentator import Instrumentator

import time
import hashlib

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting metrics collection task...")
    # Start the background task that collects metrics every 10 seconds.
    app.state.metrics_task = asyncio.create_task(collect_metrics(interval=3.0))
    yield
    # Shutdown: cancel the background task
    task = app.state.metrics_task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Metrics collection task cancelled.")

# Initialize the FastAPI app
app = FastAPI(title="ProdPulse Monitoring Service")

# Create a Prometheus gauge metric as an example
#cpu_usage = Gauge("cpu_usage_percent", "Current CPU usage in percent")

# Dummy in-memory store for current metrics
current_metrics = {
    "cpu_usage": 0.0,
    "memory_usage": 0.0,
    "disk_usage": 0.0
}

# Endpoint to retrieve current metrics
@app.get("/metrics/live", response_class=JSONResponse)
async def get_live_metrics():
    """
    Retrieve the current system metrics.
    """
    # The gauges are updated by collect_metrics; here we access their current values.
    print(cpu_usage_gauge._value.get())
    print(memory_usage_gauge._value.get())
    print(disk_usage_gauge._value.get())
    cpu_value = cpu_usage_gauge._value.get() if cpu_usage_gauge._value else 0.0
    memory_value = memory_usage_gauge._value.get() if memory_usage_gauge._value else 0.0
    disk_value = disk_usage_gauge._value.get() if disk_usage_gauge._value else 0.0

    return {
        "cpu_usage": cpu_value,
        "memory_usage": memory_value,
        "disk_usage": disk_value,
    }

# Endpoint for health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Integrate Prometheus metrics endpoint using ASGI app
# Create a separate ASGI app for Prometheus and mount it on /metrics
prometheus_app = make_asgi_app()
app.mount("/metrics", prometheus_app)


# Heavy crypto endpoint.
@app.get("/heavy", response_class=JSONResponse)
def heavy_crypto():
    """
    Performs a CPU-intensive cryptographic hashing loop that lasts at least 10 seconds.
    Returns an integer derived from the final hash digest.
    """
    start = time.time()
    # Initial data to hash.
    data = b"initial_data"
    # Continue hashing until 10 seconds have passed.
    while time.time() - start < 10:
        data = hashlib.sha256(data).digest()
    # Convert the final hash digest to an integer.
    result = int.from_bytes(data, byteorder="big")
    return {"result": result}