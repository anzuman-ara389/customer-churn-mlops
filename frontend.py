import streamlit as st
import requests

st.title("Customer Churn Prediction")

gender = st.selectbox("Gender", ["Female", "Male"])
tenure = st.number_input("Tenure", min_value=0, value=12)
monthly = st.number_input("Monthly Charges", min_value=0.0, value=79.85)
total = st.number_input("Total Charges", min_value=0.0, value=957.2)

if st.button("Predict"):
    data = {
        "gender": gender,
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": tenure,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)
    st.write(response.json())