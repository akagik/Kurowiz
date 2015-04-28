# -*- encoding: utf-8 -*-
import kdebug
import os
import os.path

from defines import CHAR_IMG_PATH
from defines import GENRE_CHAR_IMG_PATH

from klogger import logger
from PIL import Image
from kimage import *

def load_ch_barray(dirname):
    ch_dir = {}
    for path in os.listdir(dirname):
        name, ext = os.path.splitext(os.path.basename(path))
        if(len(name) == 4 or len(name) == 3):
            image = Image.open(dirname + "/" + path)
            ch_dir[unichr(int(name, 16))] = g_to_barray(image.getdata())
    return ch_dir

def list_to_str_unicode(chars):
    s = u""
    for ch in chars:
        if(ch != None):
            s += u"{0}".format(ch)
        else:
            s+=  u"□"
    return s

def genre_items_all():
    return GENRE_CH_DIR.items()

def get_genre_barray(key):
    return GENRE_CH_DIR[key]

def items_all():
    return CH_DIR.items()

def get_barray(key):
    return CH_DIR[key]


# running code ----------------------------------------------

CH_DIR = load_ch_barray(CHAR_IMG_PATH)
GENRE_CH_DIR = load_ch_barray(GENRE_CHAR_IMG_PATH)
