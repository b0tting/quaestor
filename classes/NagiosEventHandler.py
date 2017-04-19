from classes.JiraHandler import JiraHandler
from classes.TwilioHandler import TwilioHandler

class NagiosEventHandler:
    EVENT_SMS = "SMS"
    EVENT_JIRA = "JIRA"

    def __init__(self, jira_config, twilio_config):
        self.jirahandler = JiraHandler(jira_config["url"], jira_config["user"], jira_config["password"],)
        self.defaultproject = jira_config["defaultproject"]
        self.twiliohandler = TwilioHandler(twilio_config["sid"],twilio_config["auth"],twilio_config["phonenumber"])
        self.engineers = twilio_config["engineers"].split(",")

    def handle_events(self, event):
        ##events = EventDao.get_service_actions_for_event(self.event_json["service_description"])
        events = [NagiosEventHandler.EVENT_JIRA, NagiosEventHandler.EVENT_SMS]
        if NagiosEventHandler.EVENT_SMS in events:
            summary = "Quaestor event notification: " + event.get_host_name() + ":" + event.get_service_name() + " state is now " + event.get_new_state()
            for phonenumber in self.engineers:
                if phonenumber:
                    self.twiliohandler.handle_event(summary, phonenumber)

        if NagiosEventHandler.EVENT_JIRA in events:
            summary = "Quaestor event notification: " + event.get_host_name() + ":" + event.get_service_name() + " state is now " + event.get_new_state()
            description = "At " + str(event.get_time()) + ", Quaestor notified us that the service " + event.get_service_name() + " on host " + event.get_host_name() + " went into state " + event.get_new_state()
            self.jirahandler.insert_new_ticket(self.defaultproject, summary, description, "Task")