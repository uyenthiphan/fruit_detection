from flask import *
from werkzeug.utils import secure_filename
import base64
from datetime import datetime
import cv2
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from tensorflow import keras
from libraries import class_prediction, fresh_prediction
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'taken_image'

# Ensure the folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
@app.route('/')
def home_page():
    return render_template('home_page/index.html')

@app.route('/one_prediction')
def one_prediction():
    return render_template('one_prediction_start/index.html')

@app.route('/one_prediction_result',methods=["GET","POST"])
def one_prediction_result():
    fruit_class = request.args.get('fruit_class')
    fruit_status = request.args.get('fruit_status')
    class_proba = request.args.get('class_proba')
    fresh_proba = request.args.get('fresh_proba')
    return render_template('one_prediction_result/index.html',fruit_class=fruit_class,
                           fruit_status=fruit_status,class_proba=class_proba,fresh_proba=fresh_proba)

@app.route('/batch_prediction')
def batch_prediction():
    return render_template('batch_prediction_start/index.html')

@app.route('/batch_prediction_result')
def batch_prediction_result():
    return render_template('batch_prediction_result/index.html')

@app.route('/camera_capture')
def camera_capture():
    return render_template('camera_capture/index.html')

@app.route('/take_picture', methods=['POST'])
def take_picture():
    if 'photoInput' in request.form:
        data_url = request.form['photoInput']
        encoded_data = data_url.split(',')[1]
        decoded_data = base64.b64decode(encoded_data)
        # Generate a unique file name using current timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'photo_{timestamp}.jpg'

        # Specify the path where you want to save the photo
        folder_path = 'taken_image'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        # Save the decoded image data to the specified file path
        with open(file_path, 'wb') as f:
            f.write(decoded_data)
        # Redirect to a success page or return a success message
        uploaded_image_url = 'taken_image/'+file_name
        fruit_class, class_proba = class_prediction(uploaded_image_url)
        fruit_status, fresh_proba = fresh_prediction(uploaded_image_url)
        return redirect(url_for('one_prediction_result', 
                            fruit_class=fruit_class,fruit_status=fruit_status,
                            class_proba=class_proba,fresh_proba=fresh_proba))
    return 'Invalid request.'
#upload 1 photo

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'photo_{timestamp}.jpg'
    # Save the file to the "taken_image" folder
    file.save('taken_image/' + file_name)
    uploaded_image_url = 'taken_image/'+file_name
    fruit_class, class_proba = class_prediction(uploaded_image_url)
    fruit_status, fresh_proba = fresh_prediction(uploaded_image_url)
    return redirect(url_for('one_prediction_result', 
                            fruit_class=fruit_class,fruit_status=fruit_status,
                            class_proba=class_proba,fresh_proba=fresh_proba))

@app.route('/upload_batch', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return 'No file part', 400  # Return a 400 status code for bad request
    
    files = request.files.getlist('files[]')
    photo_num = 0
    file_names = []
    for file in files:
        if file.filename == '':
            continue  # Skip empty filenames
        print(file)
        photo_num += 1
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f'photo_{photo_num}_{timestamp}.jpg'
        # Save the file to the "taken_image" folder
        file.save('taken_image/' + file_name)
        file_names.append(file_name)
    
    return file_names

if __name__ == '__main__':
    app.run(debug=True)    