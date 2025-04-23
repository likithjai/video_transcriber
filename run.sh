#!/usr/bin/env bash

python transcribe.py
python new_subtitler.py
ffmpeg -hide_banner -y -i kden_out.mp4 -vf "subtitles=new_subtitles.ass" -c:a copy -preset veryslow reel.mp4
