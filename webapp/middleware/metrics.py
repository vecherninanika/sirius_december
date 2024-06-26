import time

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from webapp.metrics import DEFAULT_BUCKETS, DEPS_LATENCY

# гистограмма для измерения времени выполнения каждой ручки
API_REQUEST_LATENCY = Histogram(
    'api_request_latency_seconds',
    'Время выполнения каждой ручки в секундах',
    ['method', 'endpoint'],
    buckets=DEFAULT_BUCKETS,
)

# гистограмма для измерения времени выполнения всех интеграционных методов
INTEGRATION_METHOD_LATENCY = Histogram(
    'integration_method_latency_seconds',
    'Время выполнения всех интеграционных методов в секундах',
    ['method', 'integration_point'],
    buckets=DEFAULT_BUCKETS,
)

# счетчик для отслеживания исходящих запросов
OUTGOING_REQUESTS_COUNTER = Counter(
    'sirius_api_outgoing_requests_total',
    'Общее количество исходящих запросов от API',
    ['method', 'destination'],
)
# счетчик для отслеживания запросов
REQUESTS_COUNTER = Counter(
    'sirius_api_requests_total',
    'Общее количество запросов к API',
    ['method', 'endpoint', 'http_status'],
)

# счетчики для успешных запросов
SUCCESSFUL_REQUESTS_COUNTER = Counter(
    'sirius_api_successful_requests_total',
    'Общее количество успешных запросов к API',
    ['method', 'endpoint', 'http_status'],
)

# счетчики для неуспешных запросов
UNSUCCESSFUL_REQUESTS_COUNTER = Counter(
    'sirius_api_unsuccessful_requests_total',
    'Общее количество неудачных запросов к API',
    ['method', 'endpoint', 'http_status'],
)


class MeasureLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        endpoint = request.url.path
        method = request.method
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        DEPS_LATENCY.labels(endpoint=endpoint).observe(process_time)
        API_REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(
            process_time,
        )

        # увеличиваем счетчик
        REQUESTS_COUNTER.labels(
            method=request.method,
            endpoint=endpoint,
            http_status=response.status_code,
        ).inc()

        # увеличиваем счетчик успешных/неуспешных запросов
        if 200 <= response.status_code < 400:
            SUCCESSFUL_REQUESTS_COUNTER.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code,
            ).inc()
        else:
            UNSUCCESSFUL_REQUESTS_COUNTER.labels(
                method=request.method,
                endpoint=endpoint,
                http_status=response.status_code,
            ).inc()

        return response
