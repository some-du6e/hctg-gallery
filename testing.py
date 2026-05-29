from dotenv import load_dotenv
load_dotenv()
import os

import components.galleryManagerFrontend as gm
chat.appendStream(stream.id, PlanBlock([
	TaskCard("Searching knowledge base...", status="in_progress"),
]))
chat.appendStream(stream.id, TaskCard("Searching knowledge base...", status="complete"))
chat.appendStream(stream.id, TaskCard("Drafting response...", status="in_progress"))