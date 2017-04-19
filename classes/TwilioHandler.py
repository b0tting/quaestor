from twilio.rest import Client


class TwilioHandler:

    def __init__(self, SID, AUTH, number):
        self.client = Client(SID, AUTH)
        self.number_from = number

    def handle_event(self, text, number):
        self.client.messages.create(
            to=number,
            from_=self.number_from,
            body=text,
        )