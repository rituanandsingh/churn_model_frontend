import streamlit as st
import requests

# ── CONFIG ───────────────────────────────────────────────────────────────────
API_URL = "https://customer-churn-prediction-kyou.onrender.com"  # ← REPLACE THIS

st.set_page_config(page_title="Customer Churn Predictor", page_icon="📉", layout="centered")
st.title("📉 Customer Churn Predictor")
st.markdown("Fill in the customer details and click **Predict**.")

# ── DEMOGRAPHICS ─────────────────────────────────────────────────────────────
st.header("👤 Demographics")
col1, col2 = st.columns(2)
with col1:
    gender          = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen  = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x else "No")
with col2:
    partner    = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])

# ── PHONE SERVICE ─────────────────────────────────────────────────────────────
st.header("📞 Phone Service")
col1, col2 = st.columns(2)
with col1:
    phone_service  = st.selectbox("Phone Service", ["Yes", "No"])
with col2:
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

# ── INTERNET SERVICE ──────────────────────────────────────────────────────────
st.header("🌐 Internet & Add-ons")
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

col1, col2, col3 = st.columns(3)
with col1:
    online_security   = st.selectbox("Online Security",   ["Yes", "No", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
with col2:
    online_backup  = st.selectbox("Online Backup",  ["Yes", "No", "No internet service"])
    tech_support   = st.selectbox("Tech Support",   ["Yes", "No", "No internet service"])
with col3:
    streaming_tv     = st.selectbox("Streaming TV",     ["Yes", "No", "No internet service"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

# ── CONTRACT & BILLING ────────────────────────────────────────────────────────
st.header("📄 Contract & Billing")
col1, col2 = st.columns(2)
with col1:
    contract          = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
with col2:
    payment_method = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])

# ── CHARGES & TENURE ──────────────────────────────────────────────────────────
st.header("💰 Charges & Tenure")
col1, col2, col3 = st.columns(3)
with col1:
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0,  value=65.0,   step=0.5)
with col2:
    total_charges   = st.number_input("Total Charges ($)",   min_value=0.0, max_value=10000.0, value=1500.0, step=10.0)
with col3:
    tenure_group = st.selectbox("Tenure Group (months)", [
        "1 - 12", "13 - 24", "25 - 36", "37 - 48", "49 - 60", "61 - 72"
    ])

# ── PREDICT ───────────────────────────────────────────────────────────────────
st.markdown("---")
if st.button("🔍 Predict Churn", use_container_width=True):

    # Send RAW values — app.py does pd.get_dummies() on its side
    payload = {
        "SeniorCitizen":     senior_citizen,
        "MonthlyCharges":    monthly_charges,
        "TotalCharges":      total_charges,
        "gender":            gender,
        "Partner":           partner,
        "Dependents":        dependents,
        "PhoneService":      phone_service,
        "MultipleLines":     multiple_lines,
        "InternetService":   internet_service,
        "OnlineSecurity":    online_security,
        "OnlineBackup":      online_backup,
        "DeviceProtection":  device_protection,
        "TechSupport":       tech_support,
        "StreamingTV":       streaming_tv,
        "StreamingMovies":   streaming_movies,
        "Contract":          contract,
        "PaperlessBilling":  paperless_billing,
        "PaymentMethod":     payment_method,
        "tenure_group":      tenure_group,
    }

    with st.spinner("Contacting API… (may take ~30s on first request / cold start)"):
        try:
            response = requests.post(API_URL, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            # Your app.py returns: churn, churn_label, churn_probability
            churn_label = result.get("churn_label", "Unknown")
            probability = result.get("churn_probability", None)

            if churn_label == "Yes":
                st.error("⚠️ **Churn Prediction: YES — This customer is likely to churn!**")
            else:
                st.success("✅ **Churn Prediction: NO — This customer is likely to stay.**")

            if probability is not None:
                prob_val = float(probability)
                st.metric("Churn Probability", f"{prob_val * 100:.1f}%")
                st.progress(prob_val)

            with st.expander("📦 Raw API Response"):
                st.json(result)

        except requests.exceptions.Timeout:
            st.warning("⏱️ Timed out. The API is waking up (cold start). Wait 30s and try again.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot reach the API. Check your Render backend is running.")
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API error {response.status_code}: {e}")
            st.code(response.text)
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

st.markdown("---")
st.caption("Backend: Flask on Render · Frontend: Streamlit Community Cloud")
