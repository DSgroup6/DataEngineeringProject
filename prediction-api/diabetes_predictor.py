import os

import pandas as pd
from flask import jsonify
from google.cloud import storage
# from keras.models import load_model
from PIL import Image
from numpy import asarray
import joblib
import numpy as np
class DiabetesPredictor:
    def __init__(self):
        self.model = None

    # download the model
    def download_model(self):
        print("Lets try to download model")
        project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
        print('projectid is', project_id)
        model_repo = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
        print("model_repo is:", model_repo)
        model_name = os.environ.get('MODEL_NAME', 'Specified environment variable is not set.')
        print("model name is:", model_name)
        client = storage.Client(project=project_id)
        bucket = client.get_bucket(model_repo)
        blob = bucket.blob(model_name)
        blob.download_to_filename('local_model.pkl')
        self.model = joblib.load('local_model.pkl')
        return jsonify({'message': " the model was downloaded"}), 200

    def predict_single_record(self, file_path):
        print(file_path)
        if self.model is None:
            self.download_model()

        img = Image.open(file_path)
        img = img.convert("L")
        img_arr = asarray(img)
        img_arr = np.concatenate([[0],img_arr.flatten()]) 
        img_arr = np.subtract(np.ones(785) * 255, img_arr)
        img_arr = np.divide(img_arr, np.ones(785) * 255)
        
        # df = pd.read_json(json.dumps(prediction_input), orient='records')
        print('image data is:', img_arr)
        # y_pred = self.model.predict(img_arr)
        # print(y_pred)
        # status = (y_pred[0] > 0.5)

        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': '3'}), 200 #str(y_pred[0])
