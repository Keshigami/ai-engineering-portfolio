import os
import time
import random
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel

# Initialize metrics
REQUEST_COUNT = Counter("api_requests_total", "Total number of requests", ["endpoint", "method", "status"])
REQUEST_LATENCY = Histogram("api_request_duration_seconds", "Histogram for request latency", ["endpoint"])
PREDICTION_SCORE = Histogram("model_prediction_score", "Distribution of model prediction scores")

app = FastAPI(title="MLOps Monitoring Demo API")

# Add prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class PredictRequest(BaseModel):
    features: list[float]

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    method = request.method
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    status = response.status_code
    
    REQUEST_COUNT.labels(endpoint=endpoint, method=method, status=status).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    
    return response

@app.get("/")
async def root():
    return {"message": "Model Monitoring API is live"}

@app.post("/predict")
async def predict(request: PredictRequest):
    # Simulate model inference
    time.sleep(random.uniform(0.01, 0.1))
    prediction = random.random()
    
    PREDICTION_SCORE.observe(prediction)
    
    return {
        "prediction": prediction,
        "status": "success",
        "latency_ms": random.uniform(10, 100)
    }
