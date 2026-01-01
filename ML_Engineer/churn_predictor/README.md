# Project Title: Telecom Churn Predictor

## 1. Problem Statement & Business Impact

- **The Problem**: Telecom companies lose significant revenue when customers switch providers (churn). Identifying these customers early is critical for retention.
- **Goal**: Predict customer churn with high recall to prioritize outreach for retention campaigns.
- **Metric of Success**: Accuracy > 80%, F1-Score > 0.70.

## 2. Technical Solution

- **Approach**: Built a binary classification pipeline comparing a Logistic Regression baseline with a Random Forest champion model.
- **Stack**: Scikit-learn, Pandas, Streamlit, Matplotlib.
- **Diagram**: [Tabular Data] -> [Preprocessing] -> [Random Forest] -> [Probability Score]

## 3. Evaluation & Results

- **Performance**: Expected accuracy ~85% with synthetic data.
- **Efficiency**: Latency < 50ms per prediction.
- **Tradeoffs**: Chose Random Forest over XGBoost for this v1 for better interpretability through feature importance mapping.

## 4. Case Study Narrative

- **Context**: Demonstrates core ML fundamentals: data handling, model comparison, and business-focused dashboards.
- **Implementation**: Generated synthetic telecom data, implemented preprocessing, and built a Streamlit UI for real-time inference.
- **Limitations**: Synthetic data may not capture complex seasonal trends.
- **Next Steps**: Integrate XGBoost and deploy as a FastAPI service with monitoring.
