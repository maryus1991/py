import os
from moviepy.editor import AudioFileClip
from pydub import AudioSegment, playback
import speech_recognition as sr

def video_getter_audio_path_return(path):
    audio_of_video = AudioFileClip(path)
    file_name = str(os.path.basename(audio_of_video.filename)).replace('media/', '')
    full_path = str(os.path.abspath(path)).replace(file_name,'')
    audio_path = '{}{}.mp3'.format(full_path, file_name)
    audio_of_video.write_audiofile(audio_path)
    return audio_path


# create audio_slicer func

def audio_slicer(audio_path, start_second, end_second):
    audio_clip = AudioSegment.from_mp3(audio_path)
    sliced_part_of_audio = audio_clip[start_second:end_second + 150 ]
    audio_data = sliced_part_of_audio.raw_data
    return audio_data

def audio_translator(audio_data):
    r = sr.Recognizer()
    audio_data_one = sr.AudioData(audio_data, 441, 1)
    audio_data_two = r.record(audio_data_one.get_raw_data)
    text = r.recognize_google(audio_data_two)
    print(text)

audio_translator(audio_slicer('media/Python_WiFi_DoS_Denial_of_Service_attack.136.mp4.mp3',0 ,6 ))