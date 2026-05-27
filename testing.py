from dotenv import load_dotenv
load_dotenv()
import os

import components.images as ci
ci.uploadImage("https://placehold.co/840x420.png", 999)
