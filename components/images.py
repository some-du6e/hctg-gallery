from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from pathlib import Path
from openai import project
import requests
import boto3
import os

HCTG_BASE_URL = os.getenv("HCTG_BASE_URL", "https://game.hackclub.com")

def fakeSay(message: str):
    print(message)

def initS3Client(say=fakeSay):
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=os.getenv('CF_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('CF_SECRET_ACCESS_KEY'),
        endpoint_url=f'https://{os.getenv("CF_ACCOUNT_ID")}.r2.cloudflarestorage.com',
        region_name='auto',
    )
    say("initS3Client: initialized S3 client, returning it now...")
    return s3

def uploadImage(url, projectId: int, cli, say=fakeSay):
    response = requests.get(url)

    # get file extension
    cleanpath = urlparse(url).path
    extension = Path(cleanpath).suffix

    if response.status_code == 200:
        say(f"uploadImage: got image with 200, now uploading project {projectId} to s3...")
        cli.put_object(
        Bucket="hctg-gallery",
        Key=f"{str(projectId)}{extension}",
        Body=response.content
    )
    return extension


def uploadProjectImages(project, say=fakeSay, cli=None):
    screenshot = project.get("screenshot")
    project_id = project.get("id")
    if screenshot and project_id is not None:
        img_url = f"{HCTG_BASE_URL}{screenshot}"
        ex = uploadImage(img_url, project_id, cli, say)
        if not ex:
            say(f"uploadProjectImages: upload failed for project {project_id}, skipping screenshot update")
            return project

        img_base = os.getenv('IMG_BASE_URL')
        if not img_base:
            say("uploadProjectImages: IMG_BASE_URL not set, skipping screenshot update")
            return project

        img_base = img_base.rstrip('/')
        project["screenshot"] = f"{img_base}/{project_id}{ex}"
        return project

    


def massUploadProjectImages(projects, say=fakeSay):
    cli = initS3Client(say)
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda project: uploadProjectImages(project, say, cli), projects)

def fixImgUrl(projects, say=fakeSay):
    """Normalize project screenshot URLs.

    - If `screenshot` is empty, leave it.
    - If it already starts with http/https, leave it.
    - If it starts with IMG_BASE_URL (no scheme), add scheme
    - Otherwise, prefix with HCTG_BASE_URL.
    """
    from urllib.parse import urlparse
    for p in projects:
        sc = p.get("screenshot")
        if not sc:
            continue

        sc = str(sc).strip()
        # If it's a full URL, extract the path so uploadImage can prefix HCTG_BASE_URL
        if sc.startswith("http://") or sc.startswith("https://"):
            parsed = urlparse(sc)
            path = parsed.path or ""
            p["screenshot"] = path if path.startswith("/") else f"/{path}"
            continue

        # Ensure it starts with a single leading slash
        p["screenshot"] = sc if sc.startswith("/") else f"/{sc}"

    return projects
