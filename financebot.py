import os
from slackeventsapi import SlackEventAdapter
from slack import WebClient
import avrequest

SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_SECRET")

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")
client = WebClient(token=SLACK_BOT_TOKEN)
bot_id = "<@U011K2CV24V>"
approved_commands = ["getQuote","getWMA","getExchangeRate"]

@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print("Incoming message:")
    print(message)
    channel = message["channel"]
    if message.get("subtype") is None and bot_id in message.get('text'):
        text = message.get('text').lower()
		if text.split(" ")[0] in approved_commands:
			avrequest.router(text)
		else:
            response = "Here is a list of things you can ask me:\n"
            response += "get quote <stock_ticker> (e.g. get quote GOOG)\n"
            response += "get wma <stock_ticker> (e.g. get wma AAPL)\n"
            response += "get exchange rate <currency1> <currency2> (e.g. get exchange rate USD CAD)"
        client.chat_postMessage(
            channel=channel,
            text=response
        )


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

slack_events_adapter.start(port=3000)