
import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()

# You can also use pretrained model from Keras
# Check https://keras.io/applications/

model =tf.keras.models.load_model("saved_models/model_vgg19_v1.h5")
print('Model loaded. Check http://127.0.0.1:5000/')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    show_img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # x = np.array(x, 'float32')
    # x /= 255
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # x = x.reshape([64, 64]);
        disease_class = ['NORMAL',
                         'PNEUMONIA' ]
        CLASS_NAMES = ['NORMAL',
                         'PNEUMONIA']
        predicted_class = CLASS_NAMES[np.argmax(preds[0])]
        a = preds[0]
        ind=np.argmax(a)
        print('Prediction:', predicted_class)
        result=disease_class[ind]
        confidence = np.max(preds[0])
        # output='Class: '+predicted_class+' Accuracy: '+confidence
        return predicted_class
    return None


if __name__ == '__main__':
#     app.run(port=5002, debug=True)
    app.run(debug=False,host='0.0.0.0')
