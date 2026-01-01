import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Churn Predictor Dashboard", layout="wide")

st.title("📊 Telecom Customer Churn Predictor")
st.markdown("""
This dashboard demonstrates a baseline Logistic Regression vs. Random Forest model to predict customer churn.
**Goal**: Reduce manual triage time by identifying high-risk customers automatically.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('telecom_churn.csv')
    return df

df = load_data()

# Preprocessing
le = LabelEncoder()
df_model = df.copy()
categorical_cols = ['InternetService', 'Contract', 'PaymentMethod', 'PaperlessBilling', 'Gender', 'Partner', 'Dependents']
for col in categorical_cols:
    df_model[col] = le.fit_transform(df_model[col])

X = df_model.drop(['CustomerID', 'Churn'], axis=1)
y = df_model['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
col1, col2 = st.columns(2)

with col1:
    st.subheader("Logistic Regression (Baseline)")
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    st.text(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.2f}")
    st.text(classification_report(y_test, y_pred_lr))

with col2:
    st.subheader("Random Forest (Champion)")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    st.text(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.2f}")
    st.text(classification_report(y_test, y_pred_rf))

# Feature Importance
st.divider()
st.subheader("💡 Feature Importance (Random Forest)")
fig, ax = plt.subplots(figsize=(10, 6))
feat_importances = pd.Series(rf.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh', ax=ax, color='teal')
st.pyplot(fig)

# Prediction Section
st.divider()
st.subheader("🔮 Predict Churn for a New Customer")
with st.form("prediction_form"):
    c1, c2, c3 = st.columns(3)
    tenure = c1.slider("Tenure (Months)", 1, 72, 12)
    monthly_charge = c2.number_input("Monthly Charges ($)", value=50.0)
    contract = c3.selectbox("Contract", ['Month-to-month', 'One year', 'Two year'])
    
    submit = st.form_submit_button("Predict")
    
    if submit:
        # Mock input processing (mapping back to label encoded values)
        # Note: In a real app, you'd use a pipeline or saved encoders
        input_data = np.array([[tenure, monthly_charge, tenure*monthly_charge, 0, 0, 0, 0, 0, 0, 0, 0]])
        prediction = rf.predict(input_data)
        prob = rf.predict_proba(input_data)[0][1]
        
        if prediction[0] == 1:
            st.error(f"⚠️ High Risk of Churn ({prob:.2%})")
        else:
            st.success(f"✅ Low Risk of Churn ({prob:.2%})")
