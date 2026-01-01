import pandas as pd
import numpy as np

def generate_churn_data(n_samples=1000, seed=42):
    np.random.seed(seed)
    
    data = {
        'CustomerID': range(1, n_samples + 1),
        'Tenure': np.random.randint(1, 72, n_samples),
        'MonthlyCharges': np.random.uniform(20, 120, n_samples),
        'TotalCharges': np.zeros(n_samples),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], n_samples),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
        'Gender': np.random.choice(['Female', 'Male'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples),
        'Partner': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['Yes', 'No'], n_samples)
    }
    
    df = pd.DataFrame(data)
    df['TotalCharges'] = df['Tenure'] * df['MonthlyCharges'] + np.random.normal(0, 10, n_samples)
    
    # Churn logic (simplified)
    # Higher tenure = lower churn
    # Fiber optic = higher churn (simulating issues)
    # Month-to-month = higher churn
    churn_prob = (
        0.5 * (df['Contract'] == 'Month-to-month') +
        0.3 * (df['InternetService'] == 'Fiber optic') -
        0.2 * (df['Tenure'] > 24) +
        0.1 * (df['MonthlyCharges'] > 80)
    )
    # Normalize and add noise
    churn_prob = (churn_prob - churn_prob.min()) / (churn_prob.max() - churn_prob.min())
    df['Churn'] = (np.random.random(n_samples) < churn_prob).astype(int)
    
    return df

if __name__ == "__main__":
    df = generate_churn_data()
    df.to_csv('telecom_churn.csv', index=False)
    print("Generated telecom_churn.csv")
