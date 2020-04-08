import os
from slackeventsapi import SlackEventAdapter

slack_token = os.environ.get("SLACK_SIGNING_SECRET")
print(slack_token)

slack_events_adapter = SlackEventAdapter(slack_token, endpoint="/slack/events")

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "get" in message.get('text'):
        channel = message["channel"]
        message = ""

slack_events_adapter.start(port=3000)