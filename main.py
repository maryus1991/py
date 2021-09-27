from logging import ERROR, error
import os, sys
import time as Time
from wave import Error
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, playback
import speech_recognition as sr
import io
from termcolor import colored
from blessings import Terminal

def make_progress_bar(file_max_size, downloaded_size, 
                                    speednet='',byte_perfix='', your_message:str=' '):
    percent_not_rounded = round((downloaded_size*100)/file_max_size, 3)
    rounded_percent = int(round(percent_not_rounded,0))
    if rounded_percent <= 1 :
        rounded_percent = 1
    elif rounded_percent >= 100:
        rounded_percent = 100
    blocks = colored(chr(5775)*rounded_percent, 'green')
    percent = str(rounded_percent)+'%'
    info_result = str(downloaded_size)+'/'+str(file_max_size)
    empty_spaces = 100-rounded_percent
    if empty_spaces >= 100:
        empty_spaces = 100
    elif empty_spaces <= 1:
        empty_spaces = 1
    empty_spaces = ' '*empty_spaces
    width:int = Terminal().width 
    width : int = int(int(width)/ 2)
    bar_len = '{ %s %s } ' % (blocks, empty_spaces)
    counter_len = ' %s %s %s %s' % (percent, info_result, byte_perfix, speednet)
    if downloaded_size > file_max_size :
        print('got some problem please enter your link again ', end='\r')
    else:
        with Terminal().location(y=Terminal().height - 2):
            print(' '*(width - int(len(bar_len) / 2) + 5), bar_len ,sep=' ', end='\r', flush=True)
            with Terminal().location(y=Terminal().height -1):
                print(' '*(width - int(len(counter_len) / 2)) ,counter_len ,sep=' ', end='\r', flush=True)
            with Terminal().location(y=Terminal().height -3):
                # print(' ', end='\r')
                print(' '*(width - int(len(your_message) / 2)) ,colored(your_message, 'green') ,sep=' ', end='\r', flush=True)


def video_getter_audio_path_return(path):
    audio_of_video = AudioFileClip(path)
    file_full_name = str(os.path.basename(audio_of_video.filename)).replace('media/', '')
    full_path = str(os.path.abspath(path)).replace(file_full_name,'')
    file_name, file_perfix = os.path.splitext(file_full_name)
    audio_path = '{}.{}.mp3'.format(full_path, file_name)
    audio_of_video.write_audiofile(audio_path)
    return audio_path


def audio_slicer(audio_path, start_second, end_second):
    audio_clip = AudioSegment.from_mp3(audio_path)
    sliced_part_of_audio = audio_clip[(start_second * 1000):(end_second * 1000) + 150 ]
    audio_data = sliced_part_of_audio.raw_data
    return audio_data


def audio_translator(audio_data):
    try :    
        # print(audio_data)
        audio_sound_data = AudioSegment(audio_data,  sample_width=2, frame_rate=44100, channels=2)
        translator = sr.Recognizer()
        with sr.AudioFile(audio_sound_data.export(format='wav')) as audio_source:
        # listen for the data (load audio to memory)
            audio_data = translator.record(audio_source)
            # recognize (convert from speech to text)
            translated_sound_as_string = translator.recognize_google(audio_data)
            return translated_sound_as_string
    except : 
        return ''


def second_convertore(seconds):
    sec = seconds % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minute = sec // 60 
    sec%=60
    return "%02d:%02d:%02d" % (hour, minute, sec) 


def subtitle_file_writer(text, endtime, starttime , filepath:str):
    file_full_name = os.path.basename(filepath)
    file_name , file_perfix = os.path.splitext(file_full_name)
    file_path = filepath.replace(file_full_name, '')
    try :
        subtitle_file = open(file_path + file_name + '.srt', 'a')
    except :
        subtitle_file = open(file_path + file_name + '.srt', 'w')

    endtime_complete = second_convertore(endtime)
    starttime_complete = second_convertore(starttime)
    result_text = f'{starttime_complete} --> {endtime_complete}\n{text}\n\n' 
    subtitle_file.write(result_text)
    subtitle_file.close()
    

def main():
    first_time = Time.time()
    print('please be pation the process may take some time')
    print('please be sure to contting yo internet')
    try : 
        video_path = input('enter your video path to translate ...:')
        try: 
            audio_path = video_getter_audio_path_return(video_path)
        except:
            print('the path is wrong ...')
            sys.exit()
        video_file =  VideoFileClip(filename=video_path)
        video_durations = int(round(video_file.duration, 0))
        start_point = 0
        end_point = 2
        
        for time in range(0, video_durations, 2):
            make_progress_bar(video_durations, time, your_message= str(round((Time.time()) - first_time, 0)) + ' s')
            sliced_audio = audio_slicer(audio_path, start_point, end_point)
            translated_sound_as_text = audio_translator(sliced_audio)
            subtitle_file_writer(translated_sound_as_text, end_point, start_point, video_path)
            start_point = end_point
            end_point += 2
        print()
        os.remove(audio_path)
    except Error:
        print(Error.text)
        try :
            os.remove(audio_path)
            file_full_name = os.path.basename(video_path)
            file_name , file_perfix = os.path.splitext(file_full_name)
            file_path = video_path.replace(file_full_name, '')
            os.remove(file_path + file_name + '.srt')
        except :
            pass
    finally:
        print('we got some error please try again')
        sys.exit()




if __name__ == '__main__':
    main()