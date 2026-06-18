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

def getProjectById(projectId: int, indent: bool = False) -> any: # type: ignore # pylance-ignore
    projects = getProjects()
    for project in projects:
        if project["id"] == projectId:
            if indent:
                shitter = json.dumps(project, indent=2)
                return shitter 
            return project
    return None


def filterProjectsTuple(tags: tuple, projects: list):
    filteredProjects = []
    requiredTags = [tag for tag in tags if tag != -67]
    for project in projects:
        if all(tag in project["tags"] for tag in requiredTags):
            if -67 not in tags or project.get("high_quality", False):
                filteredProjects.append(project)
    return filteredProjects



def getFilteredProjects(tags: tuple):
    projects = getProjects()
    return filterProjectsTuple(tags, projects)


def getFilteredProjectPage(tags: tuple, pageNum: str):
    projectPage = getGalleryPage(pageNum)
    return filterProjectsTuple(tags, projectPage)



def isLastPage(pageNum: str):
    paginatedProjects = getPaginatedProjects()
    return pageNum == str(len(paginatedProjects)-1)  


def getProjectCount(text: str):
    projects = getProjects()

    if text == "cool":
        return len(projects)
    else: # this is for https://shields.io/badges/endpoint-badge
        shield = { "schemaVersion": 1, "label": text, "message": len(projects), "color": "blue" }
        return shield
