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
        response = avrequest.router(message.get('text'))
        if response == False:
            response = "Sorry, I didn't catch that. Here is a list of things you can ask me:\n"
            response += "*getQuote `<stock_ticker>` (e.g. getQuote GOOG)*\n"
            response += "*getExchangeRate `<currency1>` `<currency2>` (e.g. getExchangeRate USD CAD)*\n"
            response += "*getWMA `<stock_ticker>` (e.g. getWMA AAPL)*\n"
            response += "*search `<stock_ticker>` (e.g. search JNJ)*\n"
            response += "*getBBANDS `<stock_ticker>` (e.g. getBBANDS FB)*\n"
            response += "*getCCI `<stock_ticker>` (e.g. getCCI NFLX)*\n"
            response += "*getRating `<cryptocurrency_ticker>` (e.g. getRating BTC)*\n"
            response += "*getEMA `<stock_ticker>` (e.g. getEMA ZG)*\n"
            response += "*getOBV `<stock_ticker>` (e.g. getOBV V)*\n"
            response += "*getRSI `<stock_ticker>` (e.g. getRSI WMT)*\n"
            response += "*getSTOCK `<stock_ticker>` (e.g. getSTOCK MSFT)*\n"
            response += "*getMACD `<stock_ticker>` (e.g. getMACD ZM)*"
        client.chat_postMessage(
            channel=channel,
            text=response
        )


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

slack_events_adapter.start(port=3000)