import os.path

import boto3
import api_constant
import mp4_to_mp3_converter
from dotenv import load_dotenv

class Upload:
    load_dotenv()
    upload_service = boto3.client(
        's3',
        aws_session_token=api_constant.aws_session_token,
        aws_access_key_id=api_constant.aws_access_key_id,
        aws_secret_access_key=api_constant.aws_secret_access_key
    )

    @staticmethod
    def uploadFile(file):
        if "pdf" in os.path.basename(file):
            Upload.upload_service.upload_file(file, api_constant.bucket_name, os.path.basename(file))
