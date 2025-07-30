import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Page title and header
st.set_page_config(page_title="🏦 Bank Churn Predictor", page_icon="🤖", layout="centered")
st.title("🏦 Bank Churn Prediction App")
st.markdown("✨ Predict whether you might churn based on your banking profile!")

# Input fields
name = st.text_input('🧑 Enter Your Name', max_chars=50, placeholder='e.g., Prince')
credit_score = st.number_input("💳 Enter your credit score", min_value=50, max_value=1000)
geography = st.selectbox('🌍 Select Your Country', options=['France', 'Spain', 'Germany'], index=None, placeholder='Select Country')
gender = st.selectbox('⚧️ Select Your Gender', options=['Female', 'Male'], index=None, placeholder='Select Gender')
age = st.number_input("🎂 Enter your age", min_value=18, max_value=92)
tenure = st.number_input("📅 How long have you stayed with us (years)", min_value=0, max_value=12)
balance = st.number_input("💰 What's your balance", min_value=0.0, max_value=250898.09, step=0.01)
num_of_product = st.number_input("📦 Number of products you use", min_value=1, max_value=4)
has_card = st.selectbox("💳 Do you have a credit card?", options=['yes', 'no'], index=None, placeholder='Select option')
is_active = st.selectbox("✅ Are you active?", options=['yes', 'no'], index=None, placeholder='Select option')
estimated_salary = st.number_input("💵 Your estimated annual salary", min_value=11.58, max_value=199992.48, step=0.01)

# Predict button
button = st.button("🔍 Make Prediction")

if button:
    # Input data dictionary
    data = {
        "CreditScore": credit_score,
        "Geography": geography,
        "Gender": gender,
        "Age": age,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_of_product,
        "HasCrCard": has_card,
        "IsActiveMember": is_active,
        "EstimatedSalary": estimated_salary
    }

    df_pred = pd.DataFrame(data, index=[0])
    
    # Encode yes/no to 1/0
    df_pred['HasCrCard'] = df_pred['HasCrCard'].map({'yes': 1, 'no': 0})
    df_pred['IsActiveMember'] = df_pred['IsActiveMember'].map({'yes': 1, 'no': 0})

    # Load trained objects
    scaler = joblib.load('artifacts/scaler.pkl')
    encoder = joblib.load('artifacts/encoder.pkl')
    model = joblib.load('artifacts/model.pkl')

    # Identify numeric and categorical columns
    numeric_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
    categoric_cols = ['Geography', 'Gender']

    # Scale numeric features
    df_numeric_scaled = pd.DataFrame(scaler.transform(df_pred[numeric_cols]), columns=numeric_cols)

    # Encode categorical features
    df_categoric_encoded = pd.DataFrame(
        encoder.transform(df_pred[categoric_cols]),
        columns=encoder.get_feature_names_out(categoric_cols)
    )

    # Combine scaled & encoded features
    final_input = pd.concat([df_numeric_scaled, df_categoric_encoded], axis=1)

    # Make prediction
    prediction = model.predict(final_input)[0]
    prob_churn = model.predict_proba(final_input)[0][1]  # usually probability of churn
    prob_stay = 1 - prob_churn

    # Show result with emojis and styling
    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ **Sorry {name.title()}!** The model predicts you might **churn**.\n\n"
                 f"🔢 **Probability of churn:** `{prob_churn:.2f}`")
        st.progress(min(int(prob_churn*100), 100))
    else:
        st.success(f"✅ **Good news {name.title()}!** The model predicts you will **stay**.\n\n"
                   f"💡 **Confidence you will stay:** `{prob_stay:.2f}`")
        st.progress(min(int(prob_stay*100), 100))
    st.markdown("---")
    st.caption("🤖 *This prediction is based on the data you provided and may not be 100% accurate.*")
