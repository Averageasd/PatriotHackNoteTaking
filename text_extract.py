import os

import boto3
import api_constant


class TextExtract:
    textract_client = boto3.client('textract',
                                   region_name=api_constant.aws_default_region,
                                   aws_access_key_id=api_constant.aws_access_key_id,
                                   aws_secret_access_key=api_constant.aws_secret_access_key,
                                   aws_session_token=api_constant.aws_session_token)

    def __int__(self):
        pass

    @staticmethod
    def extract(file_name):
        print(file_name)
        response = TextExtract.textract_client.analyze_document(
            Document={'S3Object': {'Bucket': api_constant.bucket_name, 'Name': os.path.basename(file_name)}},
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

