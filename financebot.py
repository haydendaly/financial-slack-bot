import os
import slack

slack_token = os.environ.get("SLACK_BOT_TOKEN")
print(slack_token)
client = slack.WebClient(token=slack_token)

client.chat_postMessage(
  channel="#slackfinancebot",
  text="Hello from your app! :tada:"
)