import os.path

import boto3
from dotenv import load_dotenv


class Upload:
    load_dotenv()
    upload_service = boto3.client(
        's3',
        aws_session_token= os.environ.get("AWS_SESSION_TOKEN"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    @staticmethod
    def uploadFile(file):
        if "pdf" in os.path.basename(file):
            Upload.upload_service.upload_file(file, os.environ.get("BUCKET_NAME"), os.path.basename(file))
