# -*- encoding:utf-8 -*-
import kdebug
import numpy
import sys

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from defines import FONT_PATH

# mac font path /System/Library/Fonts
# ロダン　Pro M
def draw_text_at_center(img, text):
  draw = PIL.ImageDraw.Draw(img)

  draw.font = PIL.ImageFont.truetype(FONT_PATH, 20)

  img_size = numpy.array(img.size)
  txt_size = numpy.array(draw.font.getsize(text))
#  pos = (img_size - txt_size) / 2
  pos = (0, 0)
  draw.text(pos, text, 255)

def get_word_image(text):
    img = PIL.Image.new("L", (20, 20))
    draw_text_at_center(img, text)
    return img
