#!/usr/bin/env python3
import base64
from io import BytesIO
import textwrap
from os import listdir
import random

import PIL.Image
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def make_image(input_text: str, image_file=''):
    """ create an image with the given text """
    width = 1000
    height = 675
    img = Image.open(f'./faces/{image_file}')
    fnt = ImageFont.truetype('./static/oblivion_font.ttf', 25)
    text_layer = Image.new('RGBA', (width, height))
    d = ImageDraw.Draw(text_layer)
    wrapped_text = textwrap.wrap(input_text, width=100)
    padding = 15
    total_height = 0
    for line in wrapped_text:
        current_line_height = d.textsize(line, font=fnt)[1]
        total_height += current_line_height + padding
    start_height = (height - total_height) - 50
    current_height = start_height
    for line in wrapped_text:
        w, h = d.textsize(line, font=fnt)
        d.text(((width - w) / 2, current_height),
               line, font=fnt, fill='#faf5bb', stroke_width=2, stroke_fill="#000000")
        current_height += h + padding
    text_layer = text_layer.resize((1200, 675), resample=PIL.Image.BILINEAR)
    img.paste(text_layer, text_layer)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    image_string = base64.b64encode(image_bytes)
    return image_string