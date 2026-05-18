from slack_bolt.adapter.socket_mode import SocketModeHandler
import components.galleryManagerFrontend as fe
import components.jsonManager as jm
from dotenv import load_dotenv
from slack_bolt import App
import threading
import os



load_dotenv()

def formatTime(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    formatted = f"{hours}h {minutes}m"
    return formatted


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
    

    ai_declaration_1, ai_declaration_2 = {}, {}
    if project["ai_declaration"] is not None and project["ai_declaration"] != "":
        ai_declaration_1 = {
			"type": "markdown",
			"text": "---- \n ## 🤖 AI declaration\n "
	    }
        ai_declaration_2 = {
	    		"type": "markdown",
	    		"text": f"\n {project['ai_declaration']} "
	    }

    BASE_URL = "https://game.hackclub.com"
    image_url = f"{BASE_URL}/{project['screenshot']}"
    blocks = [
		{
			"type": "markdown",
			"text": f"# {project['title']} \n ### by {project['username']} \n ------\n {project['desc']} \n \n\n :clock5: {formatTime(project['real_approved_seconds'])}"
		},
		{
			"type": "image",
			"image_url": image_url,
			"alt_text": f"Screenshot of {project['title']} by {project['username']}"
		},
		ai_declaration_1,
		ai_declaration_2,
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