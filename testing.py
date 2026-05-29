from dotenv import load_dotenv
load_dotenv()
import os

import components.galleryManagerFrontend as gm
timer = gm.timer()
timer.start()
print(timer.startTime)
timer.stop()
print(timer.endTime)