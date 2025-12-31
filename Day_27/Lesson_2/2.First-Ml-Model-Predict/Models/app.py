from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load trained model
model = joblib.load("model.pkl")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Machine Failure Prediction API",
        "usage": {
            "endpoint": "/predict",
            "method": "POST",
            "example_body": {
                "temperature": 25.5,
                "vibration": 0.8,
                "pressure": 100.2
            }
        }
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    # Validate input data
    required_fields = ['temperature', 'vibration', 'pressure']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create DataFrame from input
    df = pd.DataFrame([{
        'temperature': float(data['temperature']),
        'vibration': float(data['vibration']),
        'pressure': float(data['pressure'])
    }])
    
    # Make prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    
    return jsonify({
        "prediction": int(prediction),
        "failure_probability": float(probability)
    })

if __name__ == "__main__":
    app.run( port=5000, debug=True)   
