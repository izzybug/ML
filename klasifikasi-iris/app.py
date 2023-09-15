from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('iris_knn.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        strfeatures = [x for x in request.form.values()]
        strfeatures.remove("")
        float_features = [[float(y) for y in strfeatures]]
        prediction = model.predict(float_features)
        
        if prediction == 0:
            prediction_text = "0. Sentosa"
            image_path = "static/images/setosa.jpg"
        elif prediction == 1:
            prediction_text = "1. Versicolor"
            image_path = "static/images/versicolor.jpeg"
        elif prediction == 2:
            prediction_text = "2. Virginica"
            image_path = "static/images/virginica.jpeg"
        else:
            prediction_text = "Error Classification"
            image_path = ""
        
        return render_template('index.html', prediction_text=prediction_text, image_path=image_path)
    
    return "Method Error."

if __name__ == '__main__':
    app.run(debug=True)