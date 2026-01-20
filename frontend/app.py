import streamlit as st
import requests
import json
import os

# Page Config
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="centered"
)

# Title & Description
st.title("🩺 Diabetes Progression Prediction")
st.markdown("""
This application predicts the disease progression measure based on physiological and blood serum measurements.
Enter the **real patient metrics** (unscaled) below.
""")

st.divider()

# Sidebar - API Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # In Render "API_URL" environment variable
    # If it exists, use it, otherwise use localhost
    default_url = os.getenv("API_URL", "http://diabetes_api:8000/predict")
    
    api_url = st.text_input("API URL", default_url)
    st.info("Ensure the API container is running.")

# User Input Form
col1, col2 = st.columns(2)

with col1:
    st.subheader("Physiological Data")
    # Age: Generally an integer
    age = st.number_input("Age (Years)", value=59.0, step=1.0, format="%.0f", help="Patient's age in years")
    # Sex: 1 or 2
    sex = st.number_input("Sex", value=2.0, step=1.0, format="%.0f", help="1: Male, 2: Female")
    # BMI: Can be a decimal
    bmi = st.number_input("BMI", value=32.1, step=0.1, format="%.1f", help="Body Mass Index")
    # Blood Pressure: Generally close to an integer
    bp = st.number_input("Blood Pressure (BP)", value=101.0, step=1.0, format="%.1f", help="Average Blood Pressure (mm Hg)")

with col2:
    st.subheader("Blood Serum Data")
    # s1 - s6 values for realistic ranges
    s1 = st.number_input("s1 (tc) - Total Cholesterol", value=157.0, step=1.0, format="%.1f")
    s2 = st.number_input("s2 (ldl) - Low-Density Lipoproteins", value=93.2, step=0.1, format="%.1f")
    s3 = st.number_input("s3 (hdl) - High-Density Lipoproteins", value=38.0, step=1.0, format="%.1f")
    s4 = st.number_input("s4 (tch) - Total / HDL Ratio", value=4.0, step=0.1, format="%.1f")
    # s5 logarithmic, can be small (4.0 - 6.0 is normal)
    s5 = st.number_input("s5 (ltg) - Log Serum Triglycerides", value=4.85, step=0.01, format="%.2f")
    s6 = st.number_input("s6 (glu) - Glucose", value=87.0, step=1.0, format="%.1f")

# Prediction Button
if st.button("🔍 Predict Progression", type="primary", use_container_width=True):
    input_data = {
        "age": age, "sex": sex, "bmi": bmi, "bp": bp,
        "s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6
    }
    
    with st.spinner("Consulting the AI Model..."):
        try:
            response = requests.post(api_url, json=input_data)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                
                st.success("Prediction Complete!")
                st.metric(label="Predicted Disease Progression", value=f"{prediction:.2f}")
                
                # Simple risk assessment
                if prediction < 100:
                    st.info("Low Risk Progression")
                elif prediction < 200:
                    st.warning("Moderate Progression")
                else:
                    st.error("High Progression Risk")
            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.warning("Make sure the API is running and accessible.")