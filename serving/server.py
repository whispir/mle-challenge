"""
# It starts Nginx and Gunicorn servers with specified configurations.
# The flask server is specified to be the app object in wsgi.py
#
# Web server stack:
#
#    =======          ======          =========          ===========
#   | client | <---> | Nginx | <---> | Gunicorn | <---> | Flask app |
#    =======          ======          =========          ===========
#
# Nginx: 
#   - As a web server and reverse proxy server
#   - Handle large number of simultaneous connections
#   - Face the outside world, pass requests to Gunicorn
#   - Run faster, achieve higher performance
#
# Gunicorn:
#   - Flask server not suitable for production as it doesn't scale well
#   - A WSGI server that creates multiple workers to listen and 
#       create sockets, handles http request and response
#   - Communicate with the flask app
"""
import multiprocessing
import os
import signal
import subprocess
import sys

server_workers = int(multiprocessing.cpu_count())
server_timeout = 90

def sigterm_handler(nginx_pid, gunicorn_pid):
    """ Signal termination handler
    Nginx and Gunicorn are controlled with signals
    """
    try:
        os.kill(nginx_pid, signal.SIGQUIT)
    except OSError:
        pass

    try:
        os.kill(gunicorn_pid, signal.SIGTERM)
    except OSError:
        pass

    print('Inference server shutdown.')
    sys.exit(0)


def run_server():
    """ start inference server """
    print('Starting the inference server with {} workers.'.format(server_workers))

    # link the log streams to stdout/err so they will be logged to the container logs
    subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])
    subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])

    nginx = subprocess.Popen(['nginx', '-c', '/opt/app/app_nginx.conf'])
    gunicorn = subprocess.Popen([
        'gunicorn',
        '--timeout', str(server_timeout),
        '-k', 'gevent',
        '-b', 'unix:/tmp/gunicorn.sock',
        '-w', str(server_workers),
        'wsgi:app'])

    # If either subprocess exits, the whole server process shutdown.
    pids = set([nginx.pid, gunicorn.pid])
    while True:
        pid, _ = os.wait()
        if pid in pids:
            break

    sigterm_handler(nginx.pid, gunicorn.pid)


if __name__ == '__main__':
    run_server()
