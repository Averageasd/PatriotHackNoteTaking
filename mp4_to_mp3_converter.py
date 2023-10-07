from moviepy.editor import *

filename = 'p1-video.mp4'

extracted_first_part = filename.split('.')[0]
input_video = VideoFileClip('p1-video.mp4')
input_video.audio.write_audiofile(extracted_first_part+".mp3")
