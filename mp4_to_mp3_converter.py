from moviepy.editor import *

def get_mp3_from_mp4(filename):
    extracted_first_part = os.path.basename(filename).split('.')[0]
    input_video = VideoFileClip(filename)
    input_video.audio.write_audiofile(extracted_first_part + ".mp3")
    return extracted_first_part + ".mp3"
