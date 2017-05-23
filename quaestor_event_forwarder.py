#!/usr/bin/python
import argparse
import validators
import requests
from requests import ConnectionError
from requests import HTTPError
from validators import ValidationFailure

baseurl = "/rest/event/service"

parser = argparse.ArgumentParser(description='Forward a Nagios Event to a given Quaestor instance')
parser.add_argument('QUAESTOR', help='A queastor server to call, for example "http://127.0.0.1"')
parser.add_argument('-o','--host', required=True, help='The Nagios host for the given service')
parser.add_argument('-s','--service', required=True, help='The Nagios service that changed status')
parser.add_argument('-t', '--servicestatetype', required=True, help='Weither this was a HARD or a SOFT event')
parser.add_argument('-a','--servicestate', required=True, help='The new state for this service, be it OK, WARNING, ERROR or UNKNOWN')
parser.add_argument('-v','--verbose', help='Print everything')

args = parser.parse_args()
verbose = args.verbose is not None

q_payload = {
    "host": args.host,
    "service": args.service,
    "servicestatetype":args.servicestatetype,
    "servicestate":args.servicestate,
}

if verbose:
    print("Payload: " + q_payload)
    print("Target host: " + args.QUAESTOR)

try:
    if(args.QUAESTOR.find(baseurl) == -1):
        args.QUAESTOR += baseurl

    validators.url(args.QUAESTOR)
    result = requests.post(args.QUAESTOR, json=q_payload)
    result.raise_for_status()
    json = result.json()
    if verbose:
        print(result.text)
    if not "state" in json or json["state"] != "ok":
        raise ValueError("Got an unknown or not OK answer from the Quaestor host - " + result.text)
    print("Event send succesfully - id " + json["id"])
except ValidationFailure as v:
    print(args.QUAESTOR + " was not a valid URL")
except ConnectionError as q:
    print("Could not connect to " + args.QUAESTOR)
except HTTPError as e:
    print("Got a HTTP error on sending event state: " + e.message)
except ValueError as e:
    print("Quaestor result was incorrect: " + e.message)
except Exception as e:
    print("Generic error: " + e.message)
