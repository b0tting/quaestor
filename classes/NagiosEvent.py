import datetime
from jsonschema import ValidationError
from jsonschema import validate


class NagiosEvent:
    service_json_schema = {
    "type" : "object",
        "properties" : {
            "host" : {"type" : "string"},
            "service" : {"type" : "string"},
            "servicestatetype": {"type": "string"},
            "servicestate": {"type": "string"},
        },
    }

    def __init__(self, event_json):
        try:
            validate(event_json, NagiosEvent.service_json_schema)
        except ValidationError as ve:
            raise ve
        self.event_json = event_json
        print(self.event_json)
        self.date = datetime.datetime.now()

    def get_service_name(self):
        return self.event_json["service"]

    def get_host_name(self):
        return self.event_json["host"]

    def get_servicestatetype(self):
        return self.event_json["servicestatetype"]

    def get_new_state(self):
        return self.event_json["servicestate"]

    def get_time(self):
        return self.date

