from slack_bolt.adapter.socket_mode import SocketModeHandler
import components.galleryManagerFrontend as fe
import components.jsonManager as jm
from dotenv import load_dotenv
from slack_bolt import App
from time import sleep
import threading
import random
import os


def taskCard(thing):
    return {
        "type": "task_update",
        "id": str(random.randint(0, 999999)), # should be unique per card, but doesn't need to be cryptographically secure
        "title": thing,
        "status": "complete",
    } 
load_dotenv()

def extract_project_id(input_str):
    """Extract project ID from URL, raw ID, or text containing a number."""
    import re
    from urllib.parse import urlparse
    
    input_str = input_str.strip()
    
    # If it's just a number, return it
    if input_str.isdigit():
        return input_str
    
    # If it's a URL, extract the last path segment
    if "://" in input_str:
        path = urlparse(input_str).path
        parts = path.rstrip('/').split('/')
        if parts[-1].isdigit():
            return parts[-1]
    
    # Extract any digit sequence from the text
    match = re.search(r'\d+', input_str)
    gubby = match.group(0) if match else None
    return int(gubby) if gubby else None


def formatTime(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    formatted = f"{hours}h {minutes}m"
    return formatted


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("wqdninqwio")
def message_hello(message, say, client):    
    say("dsandklsandklsandlksa")
    yo = client.chat_startStream(
        channel=message["channel"],
        thread_ts=message["ts"],
        recipient_team_id=message["team"],
        recipient_user_id=message["user"],
        icon_emoji=":thinking:",
        task_display_mode="plan",
        chunks=[{
            "type": "markdown_text",
            "text": "hello",
        }],
    )
    ts = yo["ts"]
    sleep(0.1)
    client.chat_appendStream(chunks=[taskCard("1")], channel=message["channel"], ts=ts)
    sleep(2)
    client.chat_appendStream(chunks=[taskCard("2")], channel=message["channel"], ts=ts)
    sleep(2)
    client.chat_appendStream(chunks=[taskCard("3")], channel=message["channel"], ts=ts)
    
    client.chat_stopStream(channel=message["channel"], ts=ts)




@app.command("/updategallery")
def update_gallery_command(ack, say, respond, command, logger):
    ack()
    user_id = command["user_id"]

    if user_id != os.environ.get("SLACK_ADMIN"):
        respond(
            text=f"Sorry <@{user_id}>, you don't have permission to use this command.",
            response_type="ephemeral",
        )
        return

    say(f"<@{command['user_id']}> made me update the gallery mirror")
    
    
    t = threading.Thread(target=fe.updateGalleryJSON, args=(say,))
    t.start()


# @app.command("/hellotestf")
# def testing(ack, say, command, logger):
#     ack()
#     say("hi" + f"<@{command['user_id']}>")
#     print("command: ", command)


def projectabstractionthingrllylong(say, projectId, user_id, thread_ts=None, ephemeral=False):
    say("fetching project info...", thread_ts=thread_ts)
    projectId = int(projectId)
    try:
        project = jm.getProjectById(projectId)
    except Exception as e:
        say("An error occurred while fetching the project info " + f"<@{user_id}>", ephemeral=ephemeral, thread_ts=thread_ts)
        return
    
    if project is None:
        say("No project found with that ID " + f"<@{user_id}>", ephemeral=ephemeral, thread_ts=thread_ts)
        return
    

    ai_declaration_1, ai_declaration_2 = {}, {}
    if project["ai_declaration"] is not None and project["ai_declaration"] !="":
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
    
    readme = "https://large-type.com/#not found :("
    repourl = project["repo_link"]
    demourl = project["demo_link"]
    if "github.com/" in str(repourl):
        readme = repourl + "blob/main/README.md" # todo: regex? normalising?

	# FUCK VSCODE
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
					"url": demourl
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":github: Repository"
					},
					"url": repourl
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":book: Readme"
					},
					"url": readme
				}
			]
		}
	]

    say(text=f"here's the info for project id {projectId} <@{user_id}>", thread_ts=thread_ts, ephemeral=ephemeral)
    say(
        text=f"information about project",
        blocks=blocks,
        thread_ts=thread_ts,
        ephemeral=ephemeral
    )


@app.command("/hctgprojectinfo")
@app.command("/hctgprojectinfoquiet")
def getproject(ack, say, command, logger, thread_ts=None):
	ack()
	projectooid = extract_project_id(command["text"])
	if not projectooid:
		say("Invalid project ID or URL", ephemeral=True)
		return
	projectabstractionthingrllylong(
        say=say,
        projectId=projectooid,
        user_id=command["user_id"],
        thread_ts=thread_ts,
        ephemeral=command["command"] == "/hctgprojectinfoquiet"
    )








@app.event("message")
def lookup_handler(body, logger, say, ):
    print("got msg")
    LOOKUP_CHANNEL = os.environ.get("SLACK_LOOKUP_CHANNEL")
    if body["event"]["channel"] != LOOKUP_CHANNEL: print("not lookup channel"); return
    
    # Skip events that don't have text (e.g., edited, deleted, reactions)
    if "text" not in body["event"]:
        return
    
    msg_ts = body["event"]["ts"]
    msg_text = body["event"]["text"]
    
    projectId = extract_project_id(msg_text)
    if not projectId:
        say("No valid project ID or URL found", thread_ts=msg_ts, ephemeral=True)
        return
    print(projectId)
    projectabstractionthingrllylong(
        say=say,
        projectId=projectId,
        user_id=body["event"]["user"],
        thread_ts=msg_ts,
        ephemeral=False
    )



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

def start():
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
