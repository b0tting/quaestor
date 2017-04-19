from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = '<AccountSid>'
AUTH_TOKEN = '<AuthToken>'

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to='<ToNumber>',
    from_='<FromNumber>',
    body='<BodyText>',
)