import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow import keras
import cv2
import numpy as np

def predict(a,thres=0.5):
    if a>= thres:
        return 1
    else:
        return 0
img_height, img_width = 180,180
def fresh_prediction(img_url):
    model = keras.models.load_model('model/fresh_prediction_ver4.h5')
    img = cv2.imread(img_url) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)        
    img = cv2.resize(img, (img_height, img_width))
    prediction = model.predict(np.expand_dims(img, axis=0))
    probability = prediction[0][0]
    if predict(probability) == 1:
        is_fresh = 'Fresh'
    else:
        is_fresh = 'Rotten'
        probability = 1-probability
    return is_fresh,probability

def class_prediction(img_url):
    img_height,img_width = 180,180
    model = keras.models.load_model('model/class_prediction_ver2.keras')
    img = cv2.imread(img_url) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)        
    img = cv2.resize(img, (img_height, img_width))
    class_prediction = model.predict(np.expand_dims(img, axis=0))
    class_probabilities = class_prediction[0]
    probability = max(class_probabilities)
    class_type = None
    if class_probabilities[0] == probability:
        class_type = 'Peach'
    elif class_probabilities[1] == probability:
        class_type='Pomegranate'
    else:
        class_type='Strawberry'
    return class_type,probability

class_type,probability = class_prediction('taken_image/15.jpg')
print(class_type,probability)