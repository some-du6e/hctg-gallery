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

def initS3Client():
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=os.getenv('CF_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('CF_SECRET_ACCESS_KEY'),
        endpoint_url=f'https://{os.getenv("CF_ACCOUNT_ID")}.r2.cloudflarestorage.com',
        region_name='auto',
    )
    return s3

def uploadImage(url, projectId: int):
    response = requests.get(url)
    cli = initS3Client()

    # get file extension
    cleanpath = urlparse(url).path
    extension = Path(cleanpath).suffix

    if response.status_code == 200:
        cli.put_object(
        Bucket="hctg-gallery",
        Key=f"{str(projectId)}{extension}",
        Body=response.content
    )
        


def uploadProjectImages(project):
    screenshot = project.get("screenshot")
    project_id = project.get("id")
    if screenshot and project_id is not None:
        img_url = f"{HCTG_BASE_URL}{screenshot}"
        uploadImage(img_url, project_id)


def massUploadProjectImages(projects):
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(uploadProjectImages, projects)