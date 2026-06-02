from concurrent.futures import ProcessPoolExecutor
import components.galleryManagerBackend as be
import components.images as im
from datetime import datetime
from time import sleep
import json
import os

HCTG_BASE_URL = os.getenv("HCTG_BASE_URL", "https://game.hackclub.com")
IMG_BASE_URL = os.getenv("IMG_BASE_URL", "https://r2.hctg.gallery.karimeltaib.com")

def fakeSay(message: str):
    print(message)

class timer:
    def start(self):
        self.startTime = datetime.now()
    def stop(self):
        self.endTime = datetime.now()
        self.diff = self.endTime - self.startTime
        return str(self.diff)

def fixImgUrl(projects):
    for project in projects:
        if project.get("screenshot") is not None:
            project["screenshot"] = HCTG_BASE_URL + project["screenshot"]
    return projects

def doAPage(i, say, PROJECTS, PAGINATED_PROJECTS):
    _, browser = be.initBrowser(say)
    page = browser.new_page()
    page, currentPageProjects = be.getDumpFromGalleryPage(page, i, say)

    im.massUploadProjectImages(currentPageProjects, say)

    PROJECTS.extend(currentPageProjects)
    PAGINATED_PROJECTS[i] = currentPageProjects
    sleep(1)
    page.close()

def updateGalleryJSON(say=fakeSay, important_say=fakeSay):
    important_say("Starting timer...")
    time = timer()
    time.start()

    page, _ = be.initBrowser(say)
    
    page, pages = be.getPageAmount(page, say)

    PROJECTS = []
    PAGINATED_PROJECTS = {}
    for i in range(pages):
        page, currentPageProjects = be.getDumpFromGalleryPage(page, i, say)

        im.massUploadProjectImages(currentPageProjects, say)

        PROJECTS.extend(currentPageProjects)
        PAGINATED_PROJECTS[i] = currentPageProjects

    # print(PROJECTS)
    
    say("saving projects to file")
    with open("projects.json", "w") as file:
        json.dump(PROJECTS, file)
    
    say("saving paginatated projects to file")
    with open("paginated_projects.json", "w") as file:
        json.dump(PAGINATED_PROJECTS, file)


    page, FEATURED_PROJECTS = be.getFeaturedProjects(page, say)
    say("saving featured projects to file")
    with open("featured_projects.json", "w") as file:
        json.dump(FEATURED_PROJECTS, file)
    important_say("Done updating the gallery! 🎉")
    
    stop = time.stop()
    important_say(f"Total time taken: {stop}")
    page.close()


