from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model dari file pkl
with open('knn_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    monthly_charges = float(request.form['monthly_charges'])
    paperless_billing = int(request.form['paperless_billing'])
    senior_citizen = int(request.form['senior_citizen'])
    payment_method = int(request.form['payment_method'])

    # Make prediction
    prediction = model.predict([[monthly_charges, paperless_billing, senior_citizen, payment_method]])

    # Prepare response
    if prediction[0] == 0:
        churn_status = 'No'
    else:
        churn_status = 'Yes'

    return render_template('index.html', prediction_text=f'Churn status: {churn_status}')

if __name__ == '__main__':
    app.run(debug=True)