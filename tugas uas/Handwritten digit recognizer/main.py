from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import re
import io
import base64
import keras
from keras.models import load_model

app = Flask(__name__)
model = load_model('mnist.h5')

def preprocess_image(image):
    image = image.resize((28, 28))
    image = image.convert('L')
    image = np.array(image)
    image = image.reshape(1, 28, 28, 1)
    image = image.astype('float32')
    image /= 255.0
    return image

def predict_digit(image):
    image = preprocess_image(image)
    result = model.predict(image)[0]
    digit = int(np.argmax(result))
    confidence = round(max(result) * 100, 2)
    return digit, confidence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_data = re.sub('^data:image/.+;base64,', '', request.json['image'])
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    digit, confidence = predict_digit(image)
    return jsonify({'digit': digit, 'confidence': confidence})

@app.route('/save_image', methods=['POST'])
def save_image():
    file = request.files['image']
    file.save('static/images/saved_image.png')
    return 'Image saved'

if __name__ == '__main__':
    app.run(debug=True)