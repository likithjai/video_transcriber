#!/usr/bin/env python
import time
from datetime import datetime, timedelta
import math
import ffmpeg
import whisper
from whisper.utils import get_writer

input_video = 'kden_out.mp4'

input_video_name = input_video.replace('.mp4','')

audio = f"audio-{input_video_name}.wav"

out_dir = './'

def convert(seconds):
    seconds = float(seconds)
    seconds = seconds % (24*3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02.2f" % (hour, minutes, seconds)

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream,overwrite_output=True)
    return extracted_audio


def write_srt(audio_file,out_dir):
    model = whisper.load_model('medium.en')
    whisper.DecodingOptions(language='en',
                            fp16='false',
                            task='transcribe')
    result = model.transcribe(audio_file,
                              word_timestamps=True)
    word_options = {
        'highlight_words': False,
        'max_line_count': 1,
        'max_line_width': 6
    }
    srt_writer = get_writer('srt',out_dir)
    srt_writer(result,audio_file,word_options)


def run():
    extracted_audio = extract_audio()
    write_srt(audio,out_dir)
    srt_name = audio.replace('.wav','.srt')
    ass_name = srt_name.replace('.srt','.ass')
    srt_in = ffmpeg.input(srt_name)
    out = ffmpeg.output(srt_in, ass_name).overwrite_output()
    out.run()
    f = open('subtitles.ass','r')
    header = f.readlines()[:-1]
    write_lines = []
    f = open(ass_name)
    for i, line in enumerate(f):
        if i<=len(header)-1:
            print(i, len(header)-1)
            write_lines.append(header[i])
        else:
            write_lines.append(line)
    f.close()
    with open('subtitles_final_phrase.ass','w') as f:
        f.writelines(write_lines)
            
        

    
run()


#f = open('
