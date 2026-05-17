from fastapi import FastAPI
import components.jsonManager as jm
app = FastAPI()

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



