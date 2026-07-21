from fastapi import FastAPI, HTTPException
import socket
import os
import time
from fastapi.responses import Response
from metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    ACTIVE_REQUESTS
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("general-service")

app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request, call_next):
    method = request.method
    endpoint = request.url.path

    # A request has started
    ACTIVE_REQUESTS.inc()

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        "Request completed | method=%s path=%s status=%s duration=%.3fs",
        method,
        endpoint,
        response.status_code,
        duration
    )

    # Count this request
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code)
    ).inc()

    # Record how long it took
    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)

    # Request finished
    ACTIVE_REQUESTS.dec()

    return response

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "service": "General Service",
        "hostname": socket.gethostname(),
        "company": os.getenv("COMPANY"),
        "version": os.getenv("VERSION"),
        "environment": os.getenv("ENVIRONMENT")
    }

# -----------------------------
# Liveness Probe
# -----------------------------
@app.get("/live")
def live():
    return {
        "status": "alive"
    }

# -----------------------------
# Readiness Probe
# -----------------------------
ready = True

@app.get("/ready")
def ready_check():
    if ready:
        return {
            "status": "ready"
        }

    raise HTTPException(
        status_code=503,
        detail="Service Not Ready"
    )

# -----------------------------
# Debug Endpoints
# -----------------------------
@app.post("/debug/not-ready")
def not_ready():
    global ready
    ready = False
    logger.warning("Pod marked as not READY ")
    return {
        "status": "Pod is now Not Ready"
    }

@app.post("/debug/ready")
def ready_again():
    global ready
    ready = True
    logger.warning("Pod marked as READY")
    return {
        "status": "Pod is Ready Again"
    }

# -----------------------------
# CPU Stress Test
# -----------------------------

@app.get("/cpu")
def cpu():

    logger.info("Cpu stress test started")
    end_time = time.time() + 10      # Burn CPU for 10 seconds

    x = 0

    while time.time() < end_time:
        x += 1

    logger.info("Cpu stress test completed")
    return {
        "status": "CPU work completed",
        "hostname": socket.gethostname()
    }
# -----------------------------
# Memory Leak (OOMKilled Test)
# -----------------------------
memory_store = []

@app.get("/memory")
def memory_test():
    logger.info("Memory test started")
    for _ in range(400):   # Allocate ~400 MB
        memory_store.append("A" * 1024 * 1024)
        time.sleep(0.2)

    return {"status": "Memory allocated"}


from prometheus_client import generate_latest, CONTENT_TYPE_LATEST      
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )




@app.get("/error")
def error():

    logger.error("Simulated Internal Server Error")
    raise HTTPException(
        status_code=500,
        detail="Internal Server Error"
    )