import boto3
import api_constant


class TextExtract:
    textract_client = boto3.client('textract',
                                   region_name=api_constant.aws_default_region,
                                   aws_access_key_id=api_constant.aws_access_key_id,
                                   aws_secret_access_key=api_constant.aws_secret_access_key,
                                   aws_session_token=api_constant.aws_session_token)

    # Initialize the S3 client
    # s3_client = boto3.client('s3',
    #                          region_name=api_constant.aws_default_region,
    #                          aws_access_key_id=api_constant.aws_access_key_id,
    #                          aws_secret_access_key=api_constant.aws_secret_access_key,
    #                          aws_session_token=api_constant.aws_session_token
    #                          )
    #
    # # Define your bucket name and file name
    # bucket_name = 'textract-console-us-east-1-fc6e5919-eb3d-46ef-9e60-ffaf768e7f1a'
    # file_name = 'paper.pdf'
    #
    # # Upload the PDF to S3
    # s3_client.upload_file(file_name, api_constant.bucket_name, file_name)
    #
    # # Call the analyze_document method to extract text from the PDF
    # response = textract_client.start_document_text_detection(
    #     DocumentLocation={'S3Object': {'Bucket': api_constant.bucket_name, 'Name': file_name}},
    # )
    #
    # print('JobId' in response)
    # jobId = response['JobId']
    # textract_result = None
    # while True:
    #     response = textract_client.get_document_text_detection(JobId=jobId)
    #     status = response['JobStatus']
    #
    #     if status in ['SUCCEEDED', 'FAILED']:
    #         textract_result = response
    #         break
    # print(textract_result)
    # # Initialize an empty string to store the extracted text
    # extracted_text = ""
    #
    # # Process the result and concatenate extracted text
    # for item in response["Blocks"]:
    #     if item["BlockType"] == "LINE":
    #         extracted_text += item["Text"] + " "
    #
    # with open("Output.txt", "w") as text_file:
    #     print("Output: {}".format(extracted_text), file=text_file)
    #
    # print("Text processed")

    def __int__(self):
        pass

    @staticmethod
    def extract(file_name):
        response = TextExtract.textract_client.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': api_constant.bucket_name, 'Name': file_name}},
        )

        print('JobId' in response)
        jobId = response['JobId']
        textract_result = None
        while True:
            response = TextExtract.textract_client.get_document_text_detection(JobId=jobId)
            status = response['JobStatus']

            if status in ['SUCCEEDED', 'FAILED']:
                textract_result = response
                break
        print(textract_result)
        # Initialize an empty string to store the extracted text
        extracted_text = ""

        # Process the result and concatenate extracted text
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                extracted_text += item["Text"] + " "

        with open("Output.txt", "w") as text_file:
            print("Output: {}".format(extracted_text), file=text_file)

# Initialize the Textract client with credentials
