import boto3
import openai
import os
from dotenv import load_dotenv

class Summarizer:
    # s3_client = boto3.client('s3',
    #                          region_name=api_constant.aws_default_region,
    #                          aws_access_key_id=api_constant.aws_access_key_id,
    #                          aws_secret_access_key=api_constant.aws_secret_access_key,
    #                          aws_session_token=api_constant.aws_session_token)

    # Initialize the Polly client with credentials
    load_dotenv()
    polly_client = boto3.client('polly',
                                region_name= os.environ.get("AWS_DEFAULT_REGION"),
                                aws_access_key_id= os.environ.get("AWS_ACCESS_KEY_ID"),
                                aws_secret_access_key= os.environ.get("AWS_SECRET_ACCESS_KEY"),
                                aws_session_token= os.environ.get("AWS_SESSION_TOKEN"))

    @staticmethod
    def summarize_text(text):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a college student tutor. Make a comprehensive and useful summary of the provided text. Make it look very visually appealing. Include lots of line breaks, titles, bullet points but do not use markup language. Add a TL:DR section at the end. You can add a lot of emojis, please use a lot of emojis whenever possible."},
                {"role": "user", "content": f"{text}"}
            ],
            max_tokens = 400
        )
        return response['choices'][0]['message']['content'].strip()
        # return response.choices[0].text.strip()

    @staticmethod
    def generate_video(summarized_text):
        with open("openai_summary.txt", "w") as file:
            file.write(summarized_text)
        response_male = Summarizer.polly_client.synthesize_speech(
            Text=summarized_text,
            OutputFormat="mp3",
            VoiceId="Matthew"  # You can choose a different voice if needed
        )

        # Save the synthesized speech as an MP3 file

        response_female1 = Summarizer.polly_client.synthesize_speech(
            Text=summarized_text,
            OutputFormat="mp3",
            VoiceId="Joanna"  # You can choose a different voice if needed
        )

        response_female2 = Summarizer.polly_client.synthesize_speech(
            Text=summarized_text,
            OutputFormat="mp3",
            VoiceId="Amy"  # You can choose a different voice if needed
        )

        # Save the synthesized speech as an MP3 file
        with open("polly_summary_Joanna.mp3", "wb") as f:
            f.write(response_female1["AudioStream"].read())

      # Save the synthesized speech as an MP3 file
        with open("polly_summary_Amy.mp3", "wb") as f:
            f.write(response_female2["AudioStream"].read())

        # Save the synthesized speech as an MP3 file
        with open("polly_summary_Matthew.mp3", "wb") as f:
            f.write(response_male["AudioStream"].read())
