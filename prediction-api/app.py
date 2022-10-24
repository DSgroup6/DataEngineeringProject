import os

from flask import Flask, request
from pathlib import Path
from diabetes_predictor import DiabetesPredictor
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/diabetes_predictor/model', methods=['PUT'])  # trigger updating the model
def refresh_model():
    return dp.download_model()


@app.route('/diabetes_predictor', methods=['POST'])  # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    # prediction_inout = request.get_json()
    home = str(Path.home())
    soda_home = os.path.join(home, ".service")
    if not os.path.exists(soda_home):
        os.makedirs(soda_home)
    # pfile is the name we used in the user_form.html
    if 'pfile' not in request.files:
        return jsonify({'message': 'No file part in the request'}, sort_keys=False, indent=4), 400

    file = request.files['pfile']

    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}, sort_keys=False, indent=4), 400
    else:
        # save the uploaded file locally (at the server side)
        filename = secure_filename(file.filename)
        file_path = os.path.join(soda_home, filename)
        file.save(file_path)

        try:
            return dp.predict_single_record(file_path)
        finally:
            try:
                os.remove(file_path)
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)


    # image = request.files['uploaded_file']



    


dp = DiabetesPredictor()
app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
