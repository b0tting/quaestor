import ConfigParser
import socket

import sys
import traceback
from pprint import pprint

import logging

import netifaces

import flask
from flask import Flask, jsonify
from flask import request
from jsonschema import ValidationError
from classes.NagiosEventHandler import NagiosEventHandler
from classes.NagiosEvent import NagiosEvent
from classes.QuaestorConfig import QuaestorConfig
from classes.QuaestorLogger import QuaestorLogHandler

app = Flask(__name__)

def get_my_ip():
    try:
        ip = netifaces.ifaddresses('wlan0')[2][0]['addr']
    except:
        ip = socket.gethostbyname(socket.gethostname())
    return ip


# Log file setup
configfile = "quaestor.ini"
config = ConfigParser.ConfigParser()
try:
    config.read(configfile)
except:
    print("Could not read " + configfile)
    sys.exit()

# First we set up logging with the info from the config file
logger = logging.getLogger("quaestor")
loglevel = logging.DEBUG if config.getboolean("quaestor", "debug") else logging.INFO
logger.setLevel(loglevel)
# Unless I put this up access logging will end up everywhere
#logging.getLogger('werkzeug').setLevel(loglevel)
qlh = QuaestorLogHandler()
logger.addHandler(qlh)
logger.addHandler(logging.StreamHandler())

qm = QuaestorConfig(config)
neh = NagiosEventHandler(qm)



@app.route('/rest/event/service', methods=["GET","POST"])
def handle_service_event():
    try:
        ne = NagiosEvent(request.get_json())
        try:
            neh.handle_events(ne)
        except Exception as ehe:
            traceback.print_exc()
            return jsonify({"state": "error", "message": ehe.message})
    except ValidationError as ve:
        return jsonify({"state":"validation_error","message":ve.message})
    return jsonify({"state": "ok", "id" : ne.get_id()})


@app.route('/')
def flask_show_state():
    return flask.render_template('quaestor_log.html', entries=qlh.get_last_entries(),ip=get_my_ip(), clientip=request.remote_addr)


if __name__ == '__main__':
    logger.error("Quaestor started")
    app.run(port = qm.get_quaestor_param("port"))

