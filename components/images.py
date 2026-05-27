import requests
import boto3
import os

def initS3Client():
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=os.getenv('CF_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('CF_SECRET_ACCESS_KEY'),
        endpoint_url=f'https://{os.getenv("CF_ACCOUNT_ID")}.r2.cloudflarestorage.com',
        region_name='auto',
    )
    return s3

def uploadImage(url):
    if os.exis