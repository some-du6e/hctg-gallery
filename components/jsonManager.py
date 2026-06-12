import json

def getProjects():
    with open("projects.json", "r") as file:
        return json.load(file)
    
def getFeaturedProjects():
    with open("featured_projects.json", "r") as file:
        return json.load(file)
    
def getPaginatedProjects():
    with open("paginated_projects.json", "r") as file:
        return json.load(file)
    
def getGalleryPage(pageNum: str):
    paginatedProjects = getPaginatedProjects()
    return paginatedProjects[pageNum]

def getProjectById(projectId: int, indent: bool = False):
    projects = getProjects()
    for project in projects:
        if project["id"] == projectId:
            if indent:
                return json.dumps(project, indent=2)
            return project
    return None

def isLastPage(pageNum: str):
    paginatedProjects = getPaginatedProjects()
    return pageNum == str(len(paginatedProjects)-1)  