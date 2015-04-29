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

def get_ch_dir_where(size=(20,20), width=2):
    ret = {}
    for k, v in CH_DIR.items():
        if(size[0] - width <= CH_SIZE_DIR[k][0] <= size[0] + width and
                size[1] - width <= CH_SIZE_DIR[k][1] <= size[1] + width):
            ret[k] = v
    return ret

# running code ----------------------------------------------

CH_DIR = load_ch_barray(CHAR_IMG_PATH)
GENRE_CH_DIR = load_ch_barray(GENRE_CHAR_IMG_PATH)

# 文字の大きさを定義
CH_SIZE_DIR = {}
for key, value in CH_DIR.items():
    # 半角
    if(ord(key) <= 0x203E):
        CH_SIZE_DIR[key] = (11, 14)
    # 全角
    else:
        CH_SIZE_DIR[key] = (18, 18)

CH_SIZE_DIR[u"う"] = (15, 19)
CH_SIZE_DIR[u"く"] = (12, 18)
CH_SIZE_DIR[u"し"] = (14, 18)
CH_SIZE_DIR[u"と"] = (16, 17)

CH_SIZE_DIR[u"ド"] = (12, 18)
CH_SIZE_DIR[u"フ"] = (17, 16)
CH_SIZE_DIR[u"リ"] = (13, 20)
CH_SIZE_DIR[u"レ"] = (15, 17)

CH_SIZE_DIR[u"コ"] = (16, 15)
CH_SIZE_DIR[u"エ"] = (18, 15)

CH_SIZE_DIR[u"ァ"] = (13, 13)
CH_SIZE_DIR[u"ィ"] = (13, 13)
CH_SIZE_DIR[u"ゥ"] = (13, 13)
CH_SIZE_DIR[u"ェ"] = (13, 13)
CH_SIZE_DIR[u"ォ"] = (13, 13)
CH_SIZE_DIR[u"ッ"] = (13, 13)
CH_SIZE_DIR[u"ャ"] = (13, 13)
CH_SIZE_DIR[u"ュ"] = (13, 13)
CH_SIZE_DIR[u"ョ"] = (13, 13)
CH_SIZE_DIR[u"ー"] = (18, 3)
CH_SIZE_DIR[u"、"] = (5, 7)
CH_SIZE_DIR[u"。"] = (5, 7)
CH_SIZE_DIR[u"「"] = (9, 18)
CH_SIZE_DIR[u"」"] = (9, 18)
CH_SIZE_DIR[u"『"] = (9, 18)
CH_SIZE_DIR[u"』"] = (9, 18)
CH_SIZE_DIR[u"？"] = (11, 18)

CH_SIZE_DIR[u"0"] = (9, 15)
CH_SIZE_DIR[u"1"] = (5, 15)
CH_SIZE_DIR[u"2"] = (9, 15)
CH_SIZE_DIR[u"3"] = (10, 15)
CH_SIZE_DIR[u"4"] = (10, 15)
CH_SIZE_DIR[u"5"] = (8, 14)
CH_SIZE_DIR[u"6"] = (10, 15)
CH_SIZE_DIR[u"7"] = (10, 15)
CH_SIZE_DIR[u"8"] = (10, 15)
CH_SIZE_DIR[u"9"] = (10, 15)












