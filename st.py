import streamlit as st
import numpy as np
import tensorflow as tf
import json
import base64

# Load the pre-trained model
model = tf.keras.models.load_model("customer_churn_model.h5")

# Load column names
with open("columns.json", "r") as f:
    data_columns = json.load(f)


def load_image_as_base64(image_path):
    """Convert an image file to a base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Load LinkedIn and GitHub images as base64
linkedin_image = load_image_as_base64("static/LinkedIn.png")
github_image = load_image_as_base64("static/github.png")

# Streamlit App Configuration
st.set_page_config(page_title="Customer Churn Prediction", layout="centered")

# Title and Description
st.title("Customer Churn Prediction")
st.markdown("Predict if a customer is likely to churn based on their details.")

# Sidebar for Developer Details
st.sidebar.header("Developer Details")
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <p><strong>Name:</strong> Mohd Sameer Hussain</p>
        <p><strong>Call/WhatsApp:</strong> 6303452296</p>
        <p><strong>Email:</strong> mohdsameerhussain28@gmail.com</p>
        <p>
            <a href="https://www.linkedin.com/in/mohdsameer28" target="_blank">
                <img src="data:image/png;base64,{linkedin_image}" alt="LinkedIn" style="width: 30px; height: 30px; margin-right: 10px;">
            </a>
            <a href="https://github.com/SameerHussain128?tab=repositories" target="_blank">
                <img src="data:image/png;base64,{github_image}" alt="GitHub" style="width: 30px; height: 30px;">
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# User Inputs
st.header("Enter Customer Details")
user_inputs = {}

# Dropdown Inputs for Categorical Features
user_inputs["InternetService"] = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber Optic", "No Internet Service"]
)
user_inputs["Contract"] = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two years"]
)
user_inputs["PaymentMethod"] = st.selectbox(
    "Payment Method",
    ["Bank Transfer (Automatic)", "Credit Card (Automatic)", "Electronic Check", "Mailed Check"]
)

# Integer Inputs for Other Features
for feature in data_columns:
    if feature not in [
        "InternetService_DSL", "InternetService_Fiber optic", "InternetService_No",
        "Contract_Month-to-month", "Contract_One year", "Contract_Two year",
        "PaymentMethod_Bank transfer (automatic)", "PaymentMethod_Credit card (automatic)",
        "PaymentMethod_Electronic check", "PaymentMethod_Mailed check"
    ]:
        user_inputs[feature] = st.number_input(feature, min_value=0, step=1, format="%d")

# Prediction Button
if st.button("Predict"):
    # One-hot encoding for categorical features
    input_data = [0] * len(data_columns)

    for i, col in enumerate(data_columns):
        if col in user_inputs:
            input_data[i] = user_inputs[col]
        elif col == f"InternetService_{user_inputs['InternetService']}":
            input_data[i] = 1
        elif col == f"Contract_{user_inputs['Contract']}":
            input_data[i] = 1
        elif col == f"PaymentMethod_{user_inputs['PaymentMethod']}":
            input_data[i] = 1

    # Reshape input data for the model
    input_data = np.array(input_data).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_data)
    churn_probability = prediction[0][0]

    # Display the result
    st.subheader("Prediction Result")
    if churn_probability > 0.5:
        st.write(f"The customer is likely to **Churn** with a probability of **{round(churn_probability * 100)}%**.")
    else:
        st.write(f"The customer is likely to **Stay** with a probability of **{round((1 - churn_probability) * 100)}%**.")
