# Project Title: Model-in-Prod Demo with Monitoring

## 1. Problem Statement & Business Impact

- **The Problem**: Deep learning models in production often fail silently due to data drift or performance degradation.
- **Goal**: Implement a production-grade API with real-time monitoring and alerting.
- **Metric of Success**: P99 Latency < 100ms, 100% visibility into request/error trends.

## 2. Technical Solution

- **Approach**: Built a FastAPI service with Prometheus middleware to track hardware utilization and model performance metrics.
- **Stack**: FastAPI, Prometheus, Grafana (conceptual), Python.
- **Diagram**: [Client] -> [FastAPI] -> [Prometheus Scraper] -> [Grafana Dashboard]

## 3. Evaluation & Results

- **Performance**: High availability; metrics enable proactive scaling.
- **Efficiency**: Minimal overhead from monitoring (~1ms latency impact).
- **Tradeoffs**: Chose Prometheus/FastAPI over cloud-native (AWS SageMaker) to demonstrate infrastructure-agnostic observability.

## 4. Case Study Narrative

- **Context**: Moves beyond "accuracy" to focus on "reliability" and "operability"—critical skills for AI/ML Engineers.
- **Implementation**: Instrumented a prediction endpoint to log latency, status codes, and model score distributions.
- **Limitations**: Currently runs locally; production would require a persistent metrics store like InfluxDB or Managed Prometheus.
- **Next Steps**: Integrate data drift detection (e.g., Evidently AI) to monitor feature input distributions.
