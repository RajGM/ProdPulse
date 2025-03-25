import psutil
import asyncio
from prometheus_client import Gauge

# Define Prometheus Gauges for system metrics.
cpu_usage_gauge = Gauge("cpu_usage_percent", "Current CPU usage in percent")
memory_usage_gauge = Gauge("memory_usage_percent", "Current Memory usage in percent")
disk_usage_gauge = Gauge("disk_usage_percent", "Current Disk usage in percent")

async def collect_metrics(interval: float = 10.0):
    """
    Periodically collects system metrics using psutil and updates Prometheus gauges.

    This function runs indefinitely in an asynchronous loop, capturing:
      - CPU usage percentage
      - Memory usage percentage
      - Disk usage percentage for the root partition
      
    The metrics are updated every 'interval' seconds.

    :param interval: Number of seconds between each metrics collection cycle.
    """
    while True:
        # Capture CPU usage percentage.
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_usage_gauge.set(cpu_percent)
        
        # Capture Memory usage percentage.
        memory = psutil.virtual_memory()
        memory_usage_gauge.set(memory.percent)
        
        # Capture Disk usage percentage for the root partition.
        disk = psutil.disk_usage('/')
        disk_usage_gauge.set(disk.percent)
        
        # Debug: Print collected metrics.
        print(f"Collected metrics: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%")
        
        # Wait for the specified interval before the next collection.
        await asyncio.sleep(interval)
