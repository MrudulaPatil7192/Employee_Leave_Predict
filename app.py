import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the logistic regression model
MODEL_PATH = "logistic_model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

# HTML Template with Embedded CSS
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Risk / Retention Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #311042 100%);
            --card-bg: rgba(255, 255, 255, 0.95);
            --text-main: #1E293B;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --radius: 16px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: var(--bg-gradient);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem 1rem;
        }

        .container {
            width: 100%;
            max-width: 800px;
            background: var(--card-bg);
            border-radius: var(--radius);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
            padding: 2.5rem;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .header h1 {
            color: var(--text-main);
            font-size: 1.875rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }

        .header p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.5rem;
        }

        .grid-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group label {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 0.4rem;
        }

        .form-group input, .form-group select {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1.5px solid var(--border);
            border-radius: 8px;
            font-size: 0.95rem;
            color: var(--text-main);
            background-color: #F8FAFC;
            transition: all 0.2s ease;
            outline: none;
        }

        .form-group input:focus, .form-group select:focus {
            border-color: var(--primary);
            background-color: #FFFFFF;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        .btn-submit {
            grid-column: 1 / -1;
            margin-top: 1rem;
            padding: 0.875rem;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s ease, transform 0.1s ease;
        }

        .btn-submit:hover {
            background: var(--primary-hover);
        }

        .btn-submit:active {
            transform: scale(0.99);
        }

        .result-card {
            margin-top: 2rem;
            padding: 1.25rem;
            border-radius: 12px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            animation: fadeIn 0.3s ease-in-out;
        }

        .result-class-0 {
            background-color: #DEF7EC;
            color: #03543F;
            border: 1px solid #BCF0DA;
        }

        .result-class-1 {
            background-color: #FDE8E8;
            color: #9B1C1C;
            border: 1px solid #FBD5D5;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Logistic Regression Predictor</h1>
        <p>Enter the employee details below to generate a prediction model output.</p>
    </div>

    <form method="POST" action="/predict" class="grid-form">
        <div class="form-group">
            <label for="Education">Education</label>
            <select name="Education" id="Education" required>
                <option value="Bachelors">Bachelors</option>
                <option value="Masters">Masters</option>
                <option value="PHD">PHD</option>
            </select>
        </div>

        <div class="form-group">
            <label for="JoiningYear">Joining Year</label>
            <input type="number" name="JoiningYear" id="JoiningYear" value="2015" min="2000" max="2030" required>
        </div>

        <div class="form-group">
            <label for="City">City</label>
            <select name="City" id="City" required>
                <option value="Bangalore">Bangalore</option>
                <option value="Pune">Pune</option>
                <option value="New Delhi">New Delhi</option>
            </select>
        </div>

        <div class="form-group">
            <label for="PaymentTier">Payment Tier</label>
            <select name="PaymentTier" id="PaymentTier" required>
                <option value="1">Tier 1</option>
                <option value="2">Tier 2</option>
                <option value="3" selected>Tier 3</option>
            </select>
        </div>

        <div class="form-group">
            <label for="Age">Age</label>
            <input type="number" name="Age" id="Age" value="28" min="18" max="70" required>
        </div>

        <div class="form-group">
            <label for="Gender">Gender</label>
            <select name="Gender" id="Gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
        </div>

        <div class="form-group">
            <label for="EverBenched">Ever Benched?</label>
            <select name="EverBenched" id="EverBenched" required>
                <option value="No">No</option>
                <option value="Yes">Yes</option>
            </select>
        </div>

        <div class="form-group">
            <label for="ExperienceInCurrentDomain">Experience in Current Domain (Years)</label>
            <input type="number" name="ExperienceInCurrentDomain" id="ExperienceInCurrentDomain" value="3" min="0" max="20" required>
        </div>

        <button type="submit" class="btn-submit">Predict Result</button>
    </form>

    {% if prediction_text %}
        <div class="result-card {{ result_class }}">
            {{ prediction_text }}
        </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_LAYOUT)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return render_template_string(
            HTML_LAYOUT, 
            prediction_text="Error: logistic_model.pkl not found!", 
            result_class="result-class-1"
        )

    try:
        # Extract features from form submission
        form_data = {
            "Education": request.form.get("Education"),
            "JoiningYear": int(request.form.get("JoiningYear")),
            "City": request.form.get("City"),
            "PaymentTier": int(request.form.get("PaymentTier")),
            "Age": int(request.form.get("Age")),
            "Gender": request.form.get("Gender"),
            "EverBenched": request.form.get("EverBenched"),
            "ExperienceInCurrentDomain": int(request.form.get("ExperienceInCurrentDomain"))
        }

        # Convert to DataFrame matching feature names
        input_df = pd.DataFrame([form_data])

        # Note: If your training pipeline included categorical encoders (LabelEncoder/OneHotEncoder/Scaler),
        # apply those transformations here or pass through a saved Pipeline object.
        prediction = model.predict(input_df)[0]

        result_text = f"Prediction Result: Class {prediction}"
        result_class = "result-class-0" if prediction == 0 else "result-class-1"

        return render_template_string(
            HTML_LAYOUT, 
            prediction_text=result_text, 
            result_class=result_class
        )

    except Exception as e:
        return render_template_string(
            HTML_LAYOUT, 
            prediction_text=f"Error processing input: {str(e)}", 
            result_class="result-class-1"
        )

if __name__ == "__main__":
    app.run(debug=True)
