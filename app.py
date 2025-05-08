from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os

# Load pipeline model
with open('pipeline_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load feature names from metadata (optional)
with open('model_metadata.pkl', 'rb') as file:
    model_metadata = pickle.load(file)
    feature_names = ['CreditScore', 'FirstTimeHomebuyer', 'MIP', 'DTI', 'OrigInterestRate', 'NumBorrowers',
                 'CreditScoreCategory', 'DTICategory', 'LoanRiskCategory', 'Loan_Refinance',
                 'Property_Single Family', 'Channel_R', 'PropertyState_CA', 'PropertyState_FL',
                 'PropertyState_TX', 'FirstPaymentDayOfWeek', 'FirstPaymentMonth', 'MaturityMonth',
                 'CreditRiskScore', 'Log_OrigUPB']
 # or manually define list

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            input_data = [float(request.form.get(feat)) for feat in feature_names]
            input_array = np.array(input_data).reshape(1, -1)
            prediction = model.predict(input_array)[0]
        except Exception as e:
            prediction = f"Error: {e}"
    return render_template('index.html', features=feature_names, prediction=prediction)

@app.route('/predict', methods=['POST'])
def predict_api():
    # Extract data from form fields
    input_data = [float(request.form[feature]) for feature in feature_names]
    input_data = np.array(input_data).reshape(1, -1)

    prediction = model.predict(input_data)
    return jsonify({'prediction': prediction[0]})
    print("Incoming data:", request.get_json())


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render default
    app.run(host='0.0.0.0', port=port)

