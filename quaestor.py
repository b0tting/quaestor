from flask import Flask
from flask import request

from classes import NagiosEventHandler

app = Flask(__name__)

@app.route('/rest/event/service')
def handle_service_event():
    try:
        neh = NagiosEventHandler(request.get_json())
        neh.handle_events()

    RETURN "STATE":"OK"

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
