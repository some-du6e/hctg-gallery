import components.galleryManagerBackend as be
import json

def fakeSay(message: str):
    print(message)


def updateGalleryJSON(say=fakeSay):
    
    page = be.initBrowser(say)
    
    page, pages = be.getPageAmount(page, say)

    PROJECTS = []
    PAGINATED_PROJECTS = {}
    for i in range(pages):
        page, currentPageProjects = be.getDumpFromGalleryPage(page, i, say)

        PROJECTS.extend(currentPageProjects)
        PAGINATED_PROJECTS[i] = currentPageProjects

    # print(PROJECTS)
    
    say("saving projects to file")
    with open("projects.json", "w") as file:
        json.dump(PROJECTS, file)
    
    say("saving paginatated projects to file")
    with open("paginated_projects.json", "w") as file:
        json.dump(PAGINATED_PROJECTS, file)

    say("Done updating the gallery! 🎉")


