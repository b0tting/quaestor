import datetime
from jsonschema import ValidationError
from jsonschema import validate
import uuid


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
        self.date = datetime.datetime.now()
        self.ticketnumber = False
        self.id = uuid.uuid4()

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

    def get_readeable_time(self):
        return self.date.strftime("%d %b, %H:%M")

    def set_ticket_number(self, ticketnumber):
        self.ticketnumber = ticketnumber

    def get_ticket_number(self):
        return self.ticketnumber

    def get_id(self):
        return str(self.id)
