import streamlit as st
import requests

API_URL = "https://customer-churn-prediction-kyou.onrender.com/predict"

st.set_page_config(page_title="Customer Churn Predictor", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    body { background-color: #0f172a; }
    .main { background-color: #0f172a; }
    h1 { color: #38bdf8; font-family: 'Segoe UI', sans-serif; }
    .stButton > button {
        background-color: #0ea5e9;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 2em;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 1rem;
    }
    .stButton > button:hover { background-color: #0284c7; }
    .result-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    .churn-yes { background-color: #fef2f2; color: #dc2626; border: 2px solid #dc2626; }
    .churn-no  { background-color: #f0fdf4; color: #16a34a; border: 2px solid #16a34a; }
    </style>
""", unsafe_allow_html=True)

st.title("📡 Customer Churn Predictor")
st.markdown("Fill in the customer details below to predict whether they will churn.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Demographics")
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Has Partner", ["Yes", "No"])
    dependents = st.selectbox("Has Dependents", ["Yes", "No"])

with col2:
    st.subheader("📅 Tenure & Billing")
    tenure_group = st.selectbox("Tenure Group (months)", [
        "1 - 12", "13 - 24", "25 - 36", "37 - 48", "49 - 60", "61 - 72"
    ])
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=65.0, step=0.5)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=1500.0, step=10.0)

st.divider()
st.subheader("📞 Phone & Internet Services")

col3, col4 = st.columns(2)
with col3:
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

with col4:
    online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])

col5, col6 = st.columns(2)
with col5:
    tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
with col6:
    streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

st.divider()
st.subheader("💳 Contract & Payment")

col7, col8 = st.columns(2)
with col7:
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
with col8:
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])

st.divider()

if st.button("🔍 Predict Churn"):
    payload = {
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "gender": gender,
        "Partner": partner,
        "Dependents": dependents,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "tenure_group": tenure_group,
    }

    with st.spinner("Contacting API..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=30)
            result = response.json()

            if "error" in result:
                st.error(f"API Error: {result['error']}")
            else:
                churn = result["churn_label"]
                prob = result["churn_probability"]

                css_class = "churn-yes" if churn == "Yes" else "churn-no"
                emoji = "⚠️" if churn == "Yes" else "✅"

                st.markdown(f"""
                    <div class="result-box {css_class}">
                        {emoji} Churn Prediction: <strong>{churn}</strong><br>
                        <span style="font-size:1rem; font-weight:400;">
                            Churn Probability: <strong>{prob * 100:.1f}%</strong>
                        </span>
                    </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.warning("⏳ Render free tier may be spinning up — please wait 30 seconds and try again.")
        except Exception as e:
            st.error(f"Connection error: {e}")
