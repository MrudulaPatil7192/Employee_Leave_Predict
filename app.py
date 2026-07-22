import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Logistic Regression Predictor", layout="centered")

# Custom CSS for styling the UI
st.markdown("""
    <style>
    .main {
        background-color: #0d0f1d;
    }
    .stApp {
        background-color: #121526;
    }
    .card-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #1f2937;
    }
    .title-text {
        text-align: center;
        font-weight: 700;
        font-size: 28px;
        color: #1f2937;
        margin-bottom: 5px;
    }
    .subtitle-text {
        text-align: center;
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 25px;
    }
    div.stButton > button:first-child {
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    div.stButton > button:first-child:hover {
        background-color: #4338ca;
        color: white;
    }
    .result-class-1 {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 700;
        font-size: 18px;
        margin-top: 15px;
    }
    .result-class-0 {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-weight: 700;
        font-size: 18px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Main UI Wrapper
st.markdown('<div class="title-text">Logistic Regression Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Enter the employee details below to generate a prediction model output.</div>', unsafe_allow_html=True)

# Placeholder model prediction function (Replace this with your trained model code)
def dummy_model_predict(data):
    # Replace with: return model.predict(data)[0]
    # Simple logic demonstration: if Ever Benched is Yes or Payment Tier is Tier 3 -> Class 1
    if data['EverBenched'] == 'Yes' or data['PaymentTier'] == 'Tier 3':
        return 1
    return 0

# Input Form (Prevents page reloads from clearing state)
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        education = st.selectbox("Education", ["Bachelors", "Masters", "PHD"], key="education")
        city = st.selectbox("City", ["Bangalore", "Pune", "New Delhi"], key="city")
        age = st.number_input("Age", min_value=18, max_value=70, value=28, step=1, key="age")
        ever_benched = st.selectbox("Ever Benched?", ["No", "Yes"], key="benched")

    with col2:
        joining_year = st.number_input("Joining Year", min_value=2000, max_value=2026, value=2015, step=1, key="year")
        payment_tier = st.selectbox("Payment Tier", ["Tier 1", "Tier 2", "Tier 3"], index=2, key="tier")
        gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        experience = st.number_input("Experience in Current Domain (Years)", min_value=0, max_value=40, value=3, step=1, key="experience")

    # Form Submit Button
    submit_button = st.form_submit_button(label="Predict Result")

# Output Processing & Display
if submit_button:
    # Prepare input DataFrame for model inference
    input_data = {
        'Education': education,
        'JoiningYear': joining_year,
        'City': city,
        'PaymentTier': payment_tier,
        'Age': age,
        'Gender': gender,
        'EverBenched': ever_benched,
        'ExperienceInCurrentDomain': experience
    }
    
    # Run prediction
    prediction = dummy_model_predict(input_data)

    # Dynamic styling based on class result
    if prediction == 1:
        st.markdown(
            f'<div class="result-class-1">Prediction Result: Class {prediction}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="result-class-0">Prediction Result: Class {prediction}</div>',
            unsafe_allow_html=True
        )
