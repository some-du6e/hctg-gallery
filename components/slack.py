from slack_bolt.adapter.socket_mode import SocketModeHandler
import components.galleryManagerFrontend as fe
import components.jsonManager as jm
from dotenv import load_dotenv
from slack_bolt import App
import threading
import os



load_dotenv()


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("wqdninqwio")
def message_hello(message, say, client):    
    say("dsandklsandklsandlksa")



@app.command("/updategallery")
def update_gallery_command(ack, say, command, logger):
    ack()
    say(f"<@{command['user_id']}> made me update the gallery mirror")
    
    
    t = threading.Thread(target=fe.updateGalleryJSON, args=(say,))
    t.start()


# @app.command("/hellotestf")
# def testing(ack, say, command, logger):
#     ack()
#     say("hi" + f"<@{command['user_id']}>")

@app.command("/hctgprojectinfo")
def getproject(ack, say, command, logger):
    ack()

    commandtext = command["text"]
    try:
        projectId = int(commandtext)
    except Exception as e:
        say("Please provide a valid project ID " + f"<@{command['user_id']}>")
        return

    try:
        project = jm.getProjectById(projectId)
    except Exception as e:
        say("An error occurred while fetching the project info " + f"<@{command['user_id']}>")
        return
    
    if project is None:
        say("No project found with that ID " + f"<@{command['user_id']}>")
        return
    
    blocks = [
		{
			"type": "markdown",
			"text": "# PROJECT NAME \n ### by AUTHOR \n ------\n DESCRIPTION \n \n\n :clock5: 54h4m \n :ticket: 21"
		},
		{
			"type": "image",
			"image_url": "https://placehold.co/840x420.png",
			"alt_text": "delicious tacos"
		},
		{
			"type": "markdown",
			"text": "---- \n ## 🤖 AI declaration\n "
		},
		{
			"type": "markdown",
			"text": "\n hi so i vibe coded everything bc i hate hack club and love doing hackatime f raud "
		},
		{
			"type": "markdown",
			"text": "----"
		},
		{
			"type": "actions",
			"block_id": "buttons",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "🔗 Demo"
					},
					"url": "https://api.slack.com/block-kit"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":github: Repository"
					},
					"url": "https://api.slack.com/block-kit"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":book: Readme"
					},
					"url": "https://api.slack.com/block-kit"
				}
			]
		}
	]
    say(text=f"here's the info for project id {projectId} " + f"<@{command['user_id']}>")
    say(
        text=f"information about project",
        blocks=blocks
    )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()