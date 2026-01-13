"""
Monitoring and Metrics
"""

from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

active_training_jobs = Gauge(
    'active_training_jobs',
    'Number of active training jobs'
)

models_trained_total = Counter(
    'models_trained_total',
    'Total number of models trained',
    ['model_type', 'problem_type']
)

predictions_made_total = Counter(
    'predictions_made_total',
    'Total number of predictions made',
    ['model_id']
)


def monitor_request(func):
    """Decorator to monitor API requests"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        method = 'GET'  # Default, should be extracted from request
        endpoint = func.__name__
        
        try:
            response = await func(*args, **kwargs)
            status = 'success'
            api_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            return response
        except Exception as e:
            status = 'error'
            api_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            raise
        finally:
            duration = time.time() - start_time
            api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    return wrapper
