from flask import Flask, render_template_string, request

app = Flask(__name__)

# Single-file HTML template matching your UI style
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logistic Regression Predictor</title>
    <style>
        body {
            background-color: #0d0f1d;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .card {
            background-color: #f8f9fa;
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 650px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            color: #1f2937;
        }
        h2 { text-align: center; margin-top: 0; font-size: 28px; margin-bottom: 8px; }
        p.subtitle { text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 30px; }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        .form-group { display: flex; flex-direction: column; }
        label { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
        select, input {
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            background-color: #ffffff;
            font-size: 14px;
        }
        .btn {
            background-color: #4f46e5;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            margin-top: 24px;
        }
        .btn:hover { background-color: #4338ca; }
        .result-class-1 {
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            font-size: 18px;
            margin-top: 24px;
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
            margin-top: 24px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Logistic Regression Predictor</h2>
        <p class="subtitle">Enter the employee details below to generate a prediction model output.</p>
        
        <form method="POST" action="/">
            <div class="grid">
                <div class="form-group">
                    <label>Education</label>
                    <select name="education">
                        <option value="Bachelors" {% if form_data.education == 'Bachelors' %}selected{% endif %}>Bachelors</option>
                        <option value="Masters" {% if form_data.education == 'Masters' %}selected{% endif %}>Masters</option>
                        <option value="PHD" {% if form_data.education == 'PHD' %}selected{% endif %}>PHD</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Joining Year</label>
                    <input type="number" name="joining_year" value="{{ form_data.joining_year or 2015 }}">
                </div>
                <div class="form-group">
                    <label>City</label>
                    <select name="city">
                        <option value="Bangalore" {% if form_data.city == 'Bangalore' %}selected{% endif %}>Bangalore</option>
                        <option value="Pune" {% if form_data.city == 'Pune' %}selected{% endif %}>Pune</option>
                        <option value="New Delhi" {% if form_data.city == 'New Delhi' %}selected{% endif %}>New Delhi</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Payment Tier</label>
                    <select name="payment_tier">
                        <option value="Tier 1" {% if form_data.payment_tier == 'Tier 1' %}selected{% endif %}>Tier 1</option>
                        <option value="Tier 2" {% if form_data.payment_tier == 'Tier 2' %}selected{% endif %}>Tier 2</option>
                        <option value="Tier 3" {% if form_data.payment_tier == 'Tier 3' or not form_data.payment_tier %}selected{% endif %}>Tier 3</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Age</label>
                    <input type="number" name="age" value="{{ form_data.age or 28 }}">
                </div>
                <div class="form-group">
                    <label>Gender</label>
                    <select name="gender">
                        <option value="Male" {% if form_data.gender == 'Male' %}selected{% endif %}>Male</option>
                        <option value="Female" {% if form_data.gender == 'Female' %}selected{% endif %}>Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Ever Benched?</label>
                    <select name="ever_benched">
                        <option value="No" {% if form_data.ever_benched == 'No' %}selected{% endif %}>No</option>
                        <option value="Yes" {% if form_data.ever_benched == 'Yes' %}selected{% endif %}>Yes</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Experience in Current Domain (Years)</label>
                    <input type="number" name="experience" value="{{ form_data.experience or 3 }}">
                </div>
            </div>
            
            <button type="submit" class="btn">Predict Result</button>
        </form>

        {% if prediction is not none %}
            {% if prediction == 1 %}
                <div class="result-class-1">Prediction Result: Class 1</div>
            {% else %}
                <div class="result-class-0">Prediction Result: Class 0</div>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    form_data = {}
    
    if request.method == "POST":
        form_data = request.form
        
        # Replace this dummy logic with your loaded ML model: prediction = model.predict(...)
        if form_data.get("ever_benched") == "Yes" or form_data.get("payment_tier") == "Tier 3":
            prediction = 1
        else:
            prediction = 0

    return render_template_string(HTML_TEMPLATE, prediction=prediction, form_data=form_data)

# Required by Vercel serverless build
app = app
