from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import components.jsonManager as jm
from components.www import notFound, router as www_router
# gotta keep the commit graph green
BASE_DIR = Path(__file__).resolve().parent.parent

openapi_tags = [
    {"name": "Projects", "description": "Project API endpoints"},
    {"name": "Pagination", "description": "Pagination-related endpoints"},
    {"name": "Filtering", "description": "Filtering endpoints"},
    {"name": "zFrontend", "description": "Semi hidden frontend HTML endpoints (moved to back)"},
]

app = FastAPI(openapi_tags=openapi_tags)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(www_router)

@app.get("/api/projects/{project_id}", tags=["Projects"])
def get_project(project_id):
    try:
        project_id = int(project_id)
    except Exception as e:
        return {"error": str(e)}
    
    try:
        project = jm.getProjectById(project_id, indent=True)
        return project
    except Exception as e:
        return {"error": str(e)}




@app.get("/api/projects/", tags=["Projects"])
def get_projects():
    try:
        return jm.getProjects()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/projects/page/{page_num}", tags=["Projects", "Pagination"])
def get_project_page(page_num):
    try:
        return jm.getGalleryPage(str(page_num))
    except Exception as e:
        return {"error": str(e)}





@app.get("/api/projects/filtered/page/{page_num}", tags=["Projects", "Filtering", "Pagination"])
def get_filtered_project_page(
    page_num: str,
    tags: list[int] = Query(default=[]),
):
    try:
        return jm.getFilteredProjectPage(tuple(tags), str(page_num))
    except Exception as e:
        return {"error": str(e)}



@app.get("/api/project_count", tags=["Projects", "Filtering", "Pagination"])
def get_project_count(
    change_me_for_a_shield: str = Query(default="cool"),
):
    try:
        return jm.getProjectCount(change_me_for_a_shield)
    except Exception as e:
        return {"error": str(e)}


@app.middleware("http")
async def find_404_error_codes(request, call_next):
    response = await call_next(request)

    if response.status_code == 404:
        return await notFound(request)
    return response