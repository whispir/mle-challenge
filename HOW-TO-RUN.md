# Instructions for How to Run

## Part 1: Model Training

- [ ] Build Docker image for model training: 
  - At the repository root directory, run cmd: `./build/build_training.sh`
  - It will create a Docker image called `model-training:latest`

- [ ] Test model training Docker on local machine:
  - In your cmd shell, run: `docker run -it --rm --name training model-training:latest bash`.
  - Inside the container, run: `python3 run_training.py`.
  - The training procedure and results will be printed to the screen. The **r2 score of the best model** is about `0.9`.
  - When training is finished, two files `preprocessor.joblib` and `model.joblib` will be created. They can be found by running 
  cmd `ls` inside the `/opt/app` directory.
  - To exit the container, type cmd `exit` followed by `ENTER`.
  - Alternatively, for a quick testing, you can run the cmd `./test_scripts/train_local.sh` at the repo root directory.


## Part 2: Model Serving with Flask API

- [ ] Build Docker image for model serving:
  - At the repository root directory, run cmd: `./build/build_serving.sh`
  - It will create a Docker image called `model-serving:latest`
  
- [ ] Test the serving Flask API on local machine:
  - In one cmd window, run: `docker run -p 8080:8080 -it --rm model-serving:latest`. In this way, the API server is accessible 
  via url: `http://localhost:8080`. Keep this window active.
  - Install necessary packages on local machine (Python vitural environment recemmended) by running: `pip3 install numpy pandas jsonlines requests`.
  - Open a new cmd window, run `python3 ./test_scripts/serving_test.py` at repo root directory. Test results for a couple of senarios will be printed out.


## Some Comments

### API Server Stack
A typical server stack of **Nginx + Gunicorn + Flask** is used here. Nginx is a web server and reverse proxy, while Gunicorn 
(Green Unicorn) is a Python WSGI HTTP server. The stack structure is shown below:

```
     --------         -------         ----------         -----------
    | client | <---> | Nginx | <---> | Gunicorn | <---> | Flask app |
     --------         -------         ----------         -----------
```

- Nginx: 
  - As a web server and reverse proxy server.
  - Handle large number of simultaneous connections.
  - Face the outside world, pass requests to Gunicorn.
  - Run faster, achieve higher performance.

- Gunicorn:
  - A WSGI server that creates multiple workers to listen and create sockets, handles http request and response.
  - Translates the requests from Nginx to be compatible with WSGI.
  - Communicates with the Flask app.
  
- Flask:
  - Flask server is not suitable for production as it doesn't scale well (see [here](https://flask.palletsprojects.com/en/2.0.x/deploying/index.html)).
  Thus, a server stack is a typical setup.

### Feature Engineering for Datetime

By applying *cyclical transformation*, we can convey datetime's cyclical nature to the model.
A good explanation can be found [here](https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/).
