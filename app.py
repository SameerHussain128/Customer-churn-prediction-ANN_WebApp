from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import json

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = tf.keras.models.load_model("customer_churn_model.h5")

# Load column names
with open("columns.json", "r") as f:
    data_columns = json.load(f)

@app.route("/")
def index():
    # Render the main HTML page
    return render_template("index.html", features=data_columns)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract data from request
        data = request.json

        # Map dropdown selections to one-hot encoding
        internet_service = data.get("InternetService", "InternetService_No")
        contract = data.get("Contract", "Contract_Month-to-month")
        payment_method = data.get("PaymentMethod", "PaymentMethod_Electronic check")

        # Initialize input data with zeros
        input_data = [0] * len(data_columns)

        for i, col in enumerate(data_columns):
            if col in data:
                input_data[i] = data[col]
            elif col == internet_service:
                input_data[i] = 1
            elif col == contract:
                input_data[i] = 1
            elif col == payment_method:
                input_data[i] = 1

        # Reshape input data for model
        input_data = np.array(input_data).reshape(1, -1)

        # Model prediction
        prediction = model.predict(input_data)
        churn = prediction[0][0] > 0.5

        return jsonify({
            "prediction": "Churn" if churn else "No Churn",
            "probability": float(prediction[0][0])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
