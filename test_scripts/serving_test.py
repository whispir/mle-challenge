import os
import json
import jsonlines
import requests
import pandas as pd


def test_jsonline_input(file_path, endpoint):
    ''' Test jsonlines input data '''
    headers = {'Content-Type': 'application/json'}
    with jsonlines.open(file_path) as reader:
        df = pd.DataFrame(reader)
    
    response = requests.post(endpoint, headers=headers, data=df.to_json())
    print("Prediction result for jsonlines test data: {}\n".format(response.text))


def test_csv_input(file_path, endpoint):
    ''' Test CSV input data '''
    headers = {'Content-Type': 'text/csv'}
    df = pd.read_csv(file_path)
    
    response = requests.post(endpoint, headers=headers, data=df.to_csv(index_label=False))
    print("Prediction result for csv test data: {}\n".format(response.json()))


def health_ping(endpoint):
    ''' Check whether the server is in healthy state '''
    response = requests.get(endpoint)
    print("Health ping result: {}\n".format(response.text))
    return response.status_code


def test_incorrect_content_type(file_path, endpoint):
    ''' Test unsupported content-type of http request '''
    # Specify the content-type as "text/plain"
    headers = {'Content-Type': 'text/plain'}
    df = pd.read_csv(file_path)
    
    response = requests.post(endpoint, headers=headers, data=df.to_csv(index_label=False))
    print("Response of unsupported content type: {}\n".format(response.text))


def test_undesired_data(endpoint):
    '''Use some random string as test data.

    We should be able to handle the situation where client sends 
    undesired random data which would corrupt the server.
    '''
    headers = {'Content-Type': 'application/json'}
    data = json.dumps('undesired random data ......')
    
    response = requests.post(endpoint, headers=headers, data=data)
    print("Response of the undesired data: {}\n".format(response.text))


def test_incorrect_data_schema(file_path, endpoint):
    '''Randomly rename columns for the test data.

    We should be able to handle the situation where the schema of test 
    data is different from the training dataset.
    '''
    headers = {'Content-Type': 'text/csv'}
    df = pd.read_csv(file_path)
    cols = ['col_' + str(i) for i in range(len(df.columns))]
    df = df.rename(columns={k: v for k, v in zip(df.columns, cols)})
    
    response = requests.post(endpoint, headers=headers, data=df.to_csv(index=False))
    print("Response of incorrect data schema: {}\n".format(response.text))


def test_unsupported_endpoint(file_path, endpoint):
    '''
    Test for sending request to any endpoint other than '/ping' and '/predict'.
    The supported endpoints are specified in Nginx config file.
    '''
    headers = {'Content-Type': 'text/csv'}
    df = pd.read_csv(file_path)
    
    response = requests.post(endpoint, headers=headers, data=df.to_csv(index_label=False))
    print("Response of unsupported endpoint: {}\n".format(response.text))


if __name__ == '__main__':
    CUR_DIR = os.getcwd()
    csv_file = os.path.join(CUR_DIR, "test_scripts/test_data.csv")
    jsonl_file = os.path.join(CUR_DIR, "test_scripts/test_data.jsonl")

    #PORT = 5000  # used for Flask localhost
    PORT = 8080  # used for docker container environment

    predict_endpoint = 'http://localhost:{}/predict'.format(PORT)
    ping_endpoint = 'http://localhost:{}/ping'.format(PORT)
    unsupport_endpoint = 'http://localhost:{}/hello'.format(PORT)

    health_status_code = health_ping(ping_endpoint)
    if health_status_code == 200:
        test_csv_input(csv_file, predict_endpoint)
        test_jsonline_input(jsonl_file, predict_endpoint)
        test_incorrect_content_type(csv_file, predict_endpoint)
        test_undesired_data(predict_endpoint)
        test_incorrect_data_schema(csv_file, predict_endpoint)
        test_unsupported_endpoint(csv_file, unsupport_endpoint)
    else:
        print("Flask app not working properly")
