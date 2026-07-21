from prometheus_client import Counter, Histogram, Gauge

# Total number of HTTP requests
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

# Request duration
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "endpoint"]
)

# Active requests being processed
ACTIVE_REQUESTS = Gauge(
    "http_active_requests",
    "Current Active HTTP Requests"
)