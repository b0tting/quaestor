import datetime
import os
import shutil

import pytz
import requests
from dateutil import parser

class JiraHandler:

    jiraapi = "/rest/api/2/search/"
    jiraissueapi = "/rest/api/2/issue/"

    # Niet okay! Zoveel parameters!
    def __init__(self, baseurl, username, password, recentminutes = 120):
        self.jirabase = baseurl
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.recentminutes = recentminutes

    def get_ticket_info(self, ticket):
        response = self.session.get(self.jirabase+ JiraParser.jiraissueapi + ticket)
        return response.json()

    def get_ticket_exists(self, ticket):
        response = self.session.get(self.jirabase + self.jiraissueapi + ticket)
        return response.status_code == 200

    def get_jira_response(self, query):
        response = self.session.get(self.jirabase + self.jiraapi + "?jql=" + query)
        return response.json()

    def post_jira_rest_payload(self, payload):
        response = self.session.post(self.jirabase + self.jiraissueapi, json=payload)
        return response.json()


    def get_jira_data(self, query, teamDict):
        data = self.get_jira_response(query)

        ## Now add recent info
        my_tz = "CET"
        tz = pytz.timezone(my_tz)
        today = datetime.datetime.today().date()
        recent = datetime.datetime.now(tz) - datetime.timedelta(minutes=self.recentminutes)
        if "issues" in data:
            for issue in data['issues']:
                if ("fields" in issue):
                    createdate = parser.parse(issue['fields']['created'])
                    issue['recent'] = (createdate > recent)

                    if createdate.date() == today:
                        issue["fields"]["created"] = createdate.strftime("%H:%M")
                    else:
                        issue["fields"]["created"] = createdate.strftime("%b %d")

                    key = issue["fields"]["project"]["key"].lower()
                    issue['team'] = teamDict[key] if key in teamDict.keys() else ""
        else:
            data["total"] = 0
        return data

    ## Caching JIRA images, because otherwise slow
    def get_jira_image(self, query, querystring):
        filename = "static/jiracache/" + (query + "_" + querystring).replace("/", "_")
        if not os.path.isfile(filename):
            response = self.session.get(self.jirabase + "/" + query + "?" + querystring, stream=True)
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

        with open(filename, 'rb') as out_file:
            returnimage = out_file.read()

        return returnimage


    def insert_new_ticket(self, project_key, summary, description, issuetype):
        payload = {}
        payload["fields"] = {
            "project":{"key":project_key},
            "summary": summary,
            "description": description,
            "issuetype":{"name":issuetype},
        }
        result = self.post_jira_rest_payload(payload)
        print(result)
        return result["key"]


