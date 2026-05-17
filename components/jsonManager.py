import json

def getProjects():
    with open("projects.json", "r") as file:
        return json.load(file)
    
def getPaginatedProjects():
    with open("paginated_projects.json", "r") as file:
        return json.load(file)
    
def getGalleryPage(pageNum: str):
    paginatedProjects = getPaginatedProjects()
    return paginatedProjects[pageNum]

def getProjectById(projectId: int):
    projects = getProjects()
    for project in projects:
        if project["id"] == projectId:
            return project
    return None