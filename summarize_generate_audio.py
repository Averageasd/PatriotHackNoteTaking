import boto3
import openai
import api_constant


class Summarizer:
    # s3_client = boto3.client('s3',
    #                          region_name=api_constant.aws_default_region,
    #                          aws_access_key_id=api_constant.aws_access_key_id,
    #                          aws_secret_access_key=api_constant.aws_secret_access_key,
    #                          aws_session_token=api_constant.aws_session_token)

    # Initialize the Polly client with credentials
    polly_client = boto3.client('polly',
                                region_name=api_constant.aws_default_region,
                                aws_access_key_id=api_constant.aws_access_key_id,
                                aws_secret_access_key=api_constant.aws_secret_access_key,
                                aws_session_token=api_constant.aws_session_token)

    @staticmethod
    def summarize_text(text):
        openai.api_key = api_constant.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize the provided text."},
                {"role": "user", "content": f"{text}"}
            ]
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