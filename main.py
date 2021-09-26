import os
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
# import readline as sr
# sound = sr.Recognizer()

def video_getter_audio_path_return(path):
    audio_of_video = AudioFileClip(path)
    file_name = str(os.path.basename(audio_of_video.filename)).replace('media/', '')
    full_path = str(os.path.abspath(path)).replace(file_name,'')
    audio_path = '{}{}.mp3'.format(full_path, file_name)
    audio_of_video.write_audiofile(audio_path)
    return audio_path

# create audio_slicer func
def audio_slicer(audio_path):
    audio_clip = AudioSegment.from_mp3(audio_path)
    sliced_part = (len(audio_clip) / 1000) / 5

    print(sliced_part)

audio_slicer(r'/home/maryus/Desktop/nothing/py/subtitle maker/media/Python_WiFi_DoS_Denial_of_Service_attack.136.mp4.mp3')