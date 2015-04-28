# -*- encoding:utf-8 -*-
import sys


if(sys.platform=="linux2"):
    ROOT_DIR = "/home/kohei/Project/Kurowiz"
else:
    ROOT_DIR = "/Users/kohei/Project/Kurowiz"

CH_SIM_TABLE_PATH = ROOT_DIR + "/tools/ch_sim_dir.dat"
CHAR_IMG_PATH = ROOT_DIR + "/tools/all"
GENRE_CHAR_IMG_PATH = ROOT_DIR + "/tools/genre"
QUES_PATH = ROOT_DIR + "/questions"

if(sys.platform=="linux2"):
    FONT_PATH = ROOT_DIR + "fonts/ipag.ttf"
else:
    FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴ ProN W3.otf"

TEST_LOG_PATH = ROOT_DIR + '/logs/test.log'
