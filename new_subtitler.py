#!/usr/bin/env python

from pathlib import Path
import itertools as it

def generate_pos_str(y_pos, x_pos=540):
    backslash = "\\"
    return f"{{{backslash}pos({x_pos},{y_pos})}}"

def generate_highlight_str(start_time, end_time, dialogue,
                           y_position, x_position=540,
                           layer=1, highlight_color="&HFFC000",
                           style=1):
    backslash = "\\"
    join_list = [f"Dialogue: {layer}", f"{start_time}",
                 f"{end_time}", f"style{style}",
                 '', '0', '0', '0', '',
                 generate_pos_str(y_position, x_position)+
                 f"{{{backslash}blur5{backslash}3c{highlight_color}}}{dialogue}"]
    return ','.join(join_list)

def newline_pad(line):
    if not line.endswith('\n'):
        new_line = line+'\n'
    else:
        new_line = line
    return new_line
    

in_file = Path('subtitles_final_phrase.ass')
with open(in_file, 'r') as file:
    content = file.readlines()
backslash = "\\"

y1 = generate_pos_str(1300)
y2 = generate_pos_str(1400)
y3 = generate_pos_str(1500)
style1 = "Style: style1,  Roboto Thin,  100,  &H0000FFFF, &HFF0000FF, &H00222B45, &H00000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 528, 1\n"
#style1 = "Style: style1,  Roboto Thin,  120,  &H0000FFFF, &HFF0000FF, &H00222B45, &H00000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 528, 1\n"
style2 = "Style: style2,  RobotoMono Nerd Font Mono,  100,  &H0000FFFF, &HFF0000FF, &H00222B45, &H00000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 400, 1\n"
#style2 = "Style: style2,  RobotoMono Nerd Font Mono,  120,  &H00000000, &HFF0000FF, &H00222B45, &H00000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 400, 1\n"
style3 = "Style: style3,  Roboto Black,  100,  &H00000000, &HFF0000FF, &H00222B45, &H00000000, -1, -1, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 260, 1\n"
#style3 = "Style: style3,  Roboto Black,  120,  &H00FFFFFF, &HFF0000FF, &H00222B45, &H00000000, -1, -1, 0, 0, 100, 100, 0, 0, 1, 0, 0, 2, 20, 20, 260, 1\n"
for idx, line in enumerate(content):
    if line.startswith('Dialogue'):
        first_dialogue = idx
        break
styles = it.cycle(['style1','style2','style3'])
for idx, line in enumerate(content):
    if line.startswith('Style:'):
        if 'style1' in line:
            content[idx] = style1
        if 'style2' in line:
            content[idx] = style2
            content.insert(idx+1,style3)
    if line.startswith('Dialogue:'):
        next_style = next(styles)
        content[idx] = line.replace('Default', next_style)

new_dialogues = []
for dialogue_set in it.batched(content[first_dialogue+1:], 3):
    curr_set = list(dialogue_set)
    if len(curr_set) == 3:
        first_start_time, first_end_time = curr_set[0].split(',')[1:3]
        second_end_time = curr_set[1].split(',')[2]
        last_end_time = curr_set[-1].split(',')[2]
        new_first_line = curr_set[0].replace(first_end_time, last_end_time)
        if f"{backslash}pos" not in new_first_line:
            first_line_split = new_first_line.split(',')
            new_first_line = ','.join(first_line_split[:9]) + ',' + y1 + first_line_split[9]
            dialogue = first_line_split[9]
            highlight_line = generate_highlight_str(first_start_time,
                                                    last_end_time,
                                                    dialogue, 1300)
        
        new_second_line = curr_set[1].replace(second_end_time, last_end_time)
        if f"{backslash}pos" not in new_second_line:
            second_line_split = new_second_line.split(',')
            new_second_line = ','.join(second_line_split[:9]) + ',' + y2 + second_line_split[9]
        new_third_line = curr_set[-1]
        if f"{backslash}pos" not in new_third_line:
            third_line_split = new_third_line.split(',')
            new_third_line = ','.join(third_line_split[:9]) + ',' + y3 + third_line_split[9]
        new_dialogues += [newline_pad(new_first_line), newline_pad(highlight_line), newline_pad(new_second_line), newline_pad(new_third_line)]
    else:
        new_dialogues += curr_set


new_content = content[:first_dialogue] + new_dialogues
with open('new_subtitles.ass', 'w') as f:
    f.write(''.join(new_content))

head_str = """
[Script Info]
; Comment with ";"
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,  Fontname,  Fontsize,  PrimaryColour,  SecondaryColour,  OutlineColour,  BackColour,  Bold,  Italic,  Underline,  StrikeOut,  ScaleX,  ScaleY,  Spacing,  Angle,  BorderStyle,  Outline,  Shadow,  Alignment,  MarginL,  MarginR,  MarginV,  Encoding
Style: style1,  Montserrat,  120,  &H00FFFFFF, &HFF0000FF, &H00222B45, &H00000000, -1, -1, 0, 0, 100, 100, 0, 0, 1, 4, 0, 2, 20, 20, 528, 1
Style: style2,  Recoleta,  120,  &H00FFFFFF, &HFF0000FF, &H00222B45, &H00000000, -1, -1, 0, 0, 100, 100, 0, 0, 1, 4, 0, 2, 20, 20, 400, 1
Style: style3,  Monofur Nerd Font Bold,  120,  &H00FFFFFF, &HFF0000FF, &H00222B45, &H00000000, -1, -1, 0, 0, 100, 100, 0, 0, 1, 4, 0, 2, 20, 20, 260, 1

[Events]
Format: Layer,  Start,  End,  Style,  Name,  MarginL,  MarginR,  MarginV,  Effect,  Text
"""
#Dialogue: 0,0:00:00.00,0:00:00.56,style1,,0,0,0,,If
