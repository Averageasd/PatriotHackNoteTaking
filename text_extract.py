import os
from dotenv import load_dotenv
import boto3


class TextExtract:
    load_dotenv()
    textract_client = boto3.client('textract',
                                   region_name= os.environ.get("AWS_DEFAULT_REGION"),
                                   aws_access_key_id= os.environ.get("AWS_ACCESS_KEY_ID"),
                                   aws_secret_access_key= os.environ.get("AWS_SECRET_ACCESS_KEY"),
                                   aws_session_token= os.environ.get("AWS_SESSION_TOKEN"))

    def __int__(self):
        pass

    @staticmethod
    def extract(file_name):
        print(file_name)
        response = TextExtract.textract_client.analyze_document(
            Document={'S3Object': {'Bucket': os.environ.get("BUCKET_NAME"), 'Name': os.path.basename(file_name)}},
            FeatureTypes=["TABLES", "FORMS"]
        )

        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Process the result and concatenate extracted text
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                extracted_text += item["Text"] + " "

        with open("Output.txt", "w") as text_file:
            print("Output: {}".format(extracted_text), file=text_file)

        print("Text processed")

