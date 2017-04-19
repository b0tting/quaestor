import ConfigParser

import sys
import traceback
from pprint import pprint

from flask import Flask, jsonify
from flask import request
from jsonschema import ValidationError
from classes.NagiosEventHandler import NagiosEventHandler
from classes.NagiosEvent import NagiosEvent

app = Flask(__name__)

configfile = "quaestor.ini"
config = ConfigParser.ConfigParser()
try:
    config.read(configfile)
except:
    print("Could not read " + configfile)
    sys.exit()

pprint(dict(config._sections.items()))
jiraconfig = dict(config.items('JIRA'))
twilioconfig = dict(config.items('twilio'))
twilioconfig["engineers"] = config.get("engineers", "phonenumbers")
neh = NagiosEventHandler(jiraconfig, twilioconfig)
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
    return jsonify({"state": "ok"})


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
