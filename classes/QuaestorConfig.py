class QuaestorConfig:


    def __init__(self, config):
        self.jiraconfig = dict(config.items('JIRA'))
        self.twilioconfig = dict(config.items('twilio'))
        self.twilioconfig["engineers"] = config.get("engineers", "phonenumbers").split(',')

        self.config = config


    def get_jira_parameter(self, parameter):
        return self.jiraconfig[parameter]

    def get_twilio_parameter(self, parameter):
        return self.twilioconfig[parameter]

    def get_quaestor_param(self, param):
        return self.config.get("quaestor",param)