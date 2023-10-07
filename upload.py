import os.path

import boto3
import api_constant
import mp4_to_mp3_converter
from dotenv import load_dotenv



class Upload:
    load_dotenv()
    upload_service = boto3.client(
        's3',
        aws_session_token=os.getenv('aws_session_token'),
        aws_access_key_id=os.getenv('aws_access_key_id'),
        aws_secret_access_key=os.getenv('aws_secret_access_key')
    )

    @staticmethod
    def uploadFile(file):
        if "mp4" in os.path.basename(file):
            converted_mp3 = mp4_to_mp3_converter.get_mp3_from_mp4(file)
            Upload.upload_service.upload_file(converted_mp3,
                                              api_constant.bucket_name,
                                              converted_mp3)
            os.remove(converted_mp3)
        elif "pdf" in os.path.basename(file):
            Upload.upload_service.upload_file(file, api_constant.bucket_name, os.path.basename(file))
