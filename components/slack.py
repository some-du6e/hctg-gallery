import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()
# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started

# Initializes your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("wqdninqwio")
def message_hello(message, say, client):    
    say("dsandklsandklsandlksa")



@app.command("/updategallery")
def handle_slash_command(ack, say, command, logger):
    ack()
    say(f"<@{command["user_id"]}> made me update the gallery mirror")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()