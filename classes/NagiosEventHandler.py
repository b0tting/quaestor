import json
from jsonschema import validate

class NagiosEventHandler:
    service_json_schema = {
    "type" : "object",
        "properties" : {
            "host" : {"type" : "string"},
            "service" : {"type" : "string"},
            "servicestatetype": {"type": "string"},
            "servicestate": {"type": "string"},
        },
    }

    EVENT_SMS = "SMS"
    EVENT_JIRA = "JIRA"

    def __init__(self, event_json):
        validate(event_json, NagiosEventHandler.service_json_schema)
        self.event_json - event_json


    def handle_events(self):
        events = EventDao.get_service_actions_for_event(self.event_json["service_description"])
        if NagiosEventHandler.EVENT_SMS in events:

        if NagiosEventHandler.EVENT_JIRA in events:



    def send_sms(self):