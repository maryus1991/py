import os
from moviepy.editor import AudioFileClip
from pydub import AudioSegment, playback
import speech_recognition as sr
import io

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
    # print(audio_data)
    audio_sound_data = AudioSegment(audio_data,  sample_width=2, frame_rate=44100, channels=2)
    translator = sr.Recognizer()
    with sr.AudioFile(audio_sound_data.export(format='wav')) as audio_source:
    # listen for the data (load audio to memory)
        audio_data = translator.record(audio_source)
        # recognize (convert from speech to text)
        translated_sound_as_string = translator.recognize_google(audio_data)
        return translated_sound_as_string

def subtitle_file_writer(text, endtime, starttime , filename:str):
    try :
        subtitle_file = open(filename + '.srt', 'a')
    except :
        subtitle_file = open(filename + '.srt', 'w')

    result_text = f'{starttime} --> {endtime}\n {text}' 
    subtitle_file.write(result_text)
    subtitle_file.close()


         


subtitle_file_writer(audio_translator
                    (audio_slicer
                                ('media/Python_WiFi_DoS_Denial_of_Service_attack.136.mp4.mp3',0 ,2500 )), '00:00:25', '00:00:25',
                                    'example' )