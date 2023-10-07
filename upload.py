import boto3
import api_constant

upload_service = boto3.client(
    's3',
    aws_session_token=api_constant.aws_session_token,
    aws_access_key_id=api_constant.aws_access_key_id,
    aws_secret_access_key=api_constant.aws_secret_access_key
)

file = 'samplepdf.pdf'

upload_service.upload_file(file,'textract-console-us-east-1-fc6e5919-eb3d-46ef-9e60-ffaf768e7f1a',file)

