#!/usr/bin/env python3
import base64
from io import BytesIO
import textwrap
from os import listdir
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def make_image(input_text: str, option_text=''):
    """ create an image with the given text """
    width = 1200
    height = 675
    available_faces = listdir("./faces")
    selected_face = random.choice(available_faces)
    img = Image.open(f'./faces/{selected_face}')
    top_score = 0
    options_given = option_text.upper().split()
    face_filenames = listdir('./faces/')
    random.shuffle(face_filenames)
    for file_name in face_filenames:
        if not options_given:
            break
        score = 0
        name_words = file_name.replace('.', ' ').upper().split()
        print(name_words)
        for word in name_words:
            if word in options_given:
                score += 1
        if score > top_score:
            img = Image.open(f'./faces/{file_name}')
            print(f'new best match is {file_name} with score of {score}')
            top_score = score
    fnt = ImageFont.truetype('./Kingthings Petrock.ttf', 25)
    d = ImageDraw.Draw(img)
    wrapped_text = textwrap.wrap(input_text, width=100)
    padding = 15
    total_height = 0
    for line in wrapped_text:
        current_line_height = d.textsize(line, font=fnt)[1]
        total_height += current_line_height + padding
    start_height = (height - total_height) - 50
    blurred = Image.new('RGBA', (width, height))
    blur_draw = ImageDraw.Draw(blurred)
    current_height = start_height
    for line in wrapped_text:
        w, h = d.textsize(line, font=fnt)
        blur_draw.text(((width - w) / 2, current_height),
                       line, font=fnt, fill='#74402a')
        current_height += h + padding
    blurred = blurred.filter(ImageFilter.GaussianBlur(radius=2))
    # img.paste(blurred, blurred)
    current_height = start_height
    for line in wrapped_text:
        w, h = d.textsize(line, font=fnt)
        d.text(((width - w) / 2, current_height),
               line, font=fnt, fill='#faf5bb', stroke_width=2, stroke_fill="#000000")
        current_height += h + padding
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    image_string = base64.b64encode(image_bytes)
    return image_string