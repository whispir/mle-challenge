import os
import json
import logging
import uuid
from datetime import datetime
from io import StringIO
import sys
import traceback
import flask
import pandas as pd
from joblib import load

# The flask app for serving predictions
app = flask.Flask(__name__)

app.logger.setLevel(level=logging.INFO)
CUR_DIR = os.getcwd()

def get_model():
    """ Get model object """
    model = load(os.path.join(CUR_DIR, "model.joblib"))
    return model

def get_preprocessor():
    """ Get preprocessor object """
    pre = load(os.path.join(CUR_DIR, "preprocessor.joblib"))
    return pre

def incorrect_data_response():
    return flask.Response(response="Please ensure input data is in correct format",
        status=400, mimetype='text/plain')


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. 
    We declare it is healthy if we can load the model successfully.
    """
    health = False
    try:
        get_model()
        get_preprocessor()
        health = True
    except:
        pass

    status = 200 if health else 404
    resp = 'OK' if health else 'Flask server not available'
    return flask.Response(response=resp, status=status, mimetype='application/json')


@app.route('/predict', methods=['POST'])
def prediction():
    '''The predict endpoint'''
    data = None
    result = []
    supported_json = ['application/json', 'application/jsonlines', 'application/jsonl']

    if flask.request.mimetype == 'text/csv':
        try:
            charset = flask.request.mimetype_params.get('charset', 'utf-8')
            data = flask.request.data.decode(charset)
            stream = StringIO(data)
            df = pd.read_csv(stream)
        except Exception as e:
            return incorrect_data_response()
    elif flask.request.mimetype in supported_json:
        try:
            charset = flask.request.mimetype_params.get('charset', 'utf-8')
            data = flask.request.data.decode(charset)
            stream = StringIO(data)
            df = pd.read_json(stream)
        except Exception as e:
            return incorrect_data_response()
    else:
        return flask.Response(
            response='The predictor only supports CSV, JSON and JSON lines data', 
            status=415, mimetype='text/plain')
    
    model = get_model()
    preprocessor = get_preprocessor()

    try:
        processed_df = preprocessor.fit_transform(df)
        result = model.predict(processed_df)
        out = StringIO()
        json.dump({'prediction': list(result)}, out)
        predicted = out.getvalue()

        flask_response = predicted
        flask_status = 200
        flask_mimetype = 'application/json'
    except Exception as e: 
        traceback.print_exc()
        flask_response = json.dumps({'error': str(e)})
        flask_status = 500
        flask_mimetype = 'application/json'

    request_id = str(uuid.uuid4())
    rows_count = df.shape[0]
    info = {
        "timestamp": datetime.now().isoformat(),
        "request_id": request_id,
        "request_size_in_bytes": sys.getsizeof(data),
        "response_http_status_code": flask_status,
        "error_message": flask_response if flask_status == 500 else None,
        "rows_count": rows_count,
        "prediction_output": json.dumps(list(result))
    }
    app.logger.info(info)
    
    return flask.Response(response=flask_response, status=flask_status, mimetype=flask_mimetype)
