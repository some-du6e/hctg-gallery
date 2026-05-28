from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import components.jsonManager as jm
from components.www import router as www_router
# gotta keep the commit graph green
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(www_router)

@app.get("/api/projects/{project_id}")
def get_project(project_id):
    try:
        project_id = int(project_id)
    except Exception as e:
        return {"error": str(e)}
    
    try:
        return jm.getProjectById(project_id)
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/api/projects/")
def get_projects():
    try:
        return jm.getProjects()
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/projects/page/{page_num}")
def get_project_page(page_num):
    try:
        return jm.getGalleryPage(str(page_num))
    except Exception as e:
        return {"error": str(e)}

