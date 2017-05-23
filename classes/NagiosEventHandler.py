import logging

from classes.JiraHandler import JiraHandler
from classes.TwilioHandler import TwilioHandler

logger = logging.getLogger("quaestor")


class NagiosEventHandler:
    EVENT_SMS = "SMS"
    EVENT_JIRA = "JIRA"

    def __init__(self, quaestorconfig):
        self.config = quaestorconfig
        self.jirahandler = JiraHandler(self.config.get_jira_parameter("url"), self.config.get_jira_parameter("user"), self.config.get_jira_parameter("password"),)
        self.twiliohandler = TwilioHandler(self.config.get_twilio_parameter("sid"), self.config.get_twilio_parameter("auth"), self.config.get_twilio_parameter("phonenumber"))

    def handle_events(self, event):
        ##events = EventDao.get_service_actions_for_event(self.event_json["service_description"])
        events = [NagiosEventHandler.EVENT_JIRA, NagiosEventHandler.EVENT_SMS]
        ##events = [NagiosEventHandler.EVENT_JIRA]
        logger.info("Got event " + event.get_id() + " - " + event.get_service_name() + " / " + event.get_host_name())


        if NagiosEventHandler.EVENT_JIRA in events:
            summary = "Quaestor notification: " + event.get_service_name() + " at "  + event.get_host_name() + " state is now " + event.get_new_state()
            description = "At " + event.get_readeable_time() + ", Quaestor notified us that the service " + event.get_service_name() + " on host " + event.get_host_name() + " went into state " + event.get_new_state()
            ticketnumber = self.jirahandler.insert_new_ticket(self.config.get_jira_parameter("defaultproject"), summary, description, self.config.get_jira_parameter("issuetype"))
            event.set_ticket_number(ticketnumber)
            logger.info("Logged event " + event.get_id() + " in JIRA ticket " + event.get_ticket_number())

        if NagiosEventHandler.EVENT_SMS in events:
            summary = "Quaestor event: " + event.get_service_name() + " at " + event.get_host_name()  + " state is now " + event.get_new_state()
            if event.get_ticket_number():
                summary += " - (" + self.jirahandler.get_ticket_url(event.get_ticket_number()) + ")"
            for phonenumber in self.config.get_twilio_parameter("engineers"):
                if phonenumber:
                    self.twiliohandler.handle_event(summary, phonenumber)

