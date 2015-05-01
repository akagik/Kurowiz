# -*- encoding: utf-8 -*-
#execfile('/home/kohei/.pystartup')

import sys
from defines import ROOT_DIR
from klogger import logger
from PIL import Image
import os

SELECT_ANSWER_POS = []
SELECT_ANSWER_POS.append((233, 254))
SELECT_ANSWER_POS.append((233, 191))
SELECT_ANSWER_POS.append((233, 129))
SELECT_ANSWER_POS.append((233,  66))

SELECT_GENRE_POS = []
SELECT_GENRE_POS.append((150, 220))
SELECT_GENRE_POS.append((330, 220))
SELECT_GENRE_POS.append((150, 90))
SELECT_GENRE_POS.append((330, 90))

# ゲームウィンドウの左下の点
WINDOW_ORIGIN = (480, 769) # origin position


#window_origin = (480, 780)
#window_origin = (946, 769)

WINDOW_WIDTH = 448
WINDOW_HEIGHT = 714
ORIGINAL_WINDOW_SIZE = (448, 714)

# ゲームウィンドウの右上の点
#window_righttop = (480 + 448, 769 - 714) # origin position
WINDOW_RIGHTTOP = (
        WINDOW_ORIGIN[0] + WINDOW_WIDTH,
        WINDOW_ORIGIN[1] - WINDOW_HEIGHT
        )

ASPECT_RATIO = (
        float(WINDOW_WIDTH) / ORIGINAL_WINDOW_SIZE[0],
        float(WINDOW_HEIGHT) / ORIGINAL_WINDOW_SIZE[1]
        )

# multi window
WINDOW_ORIGINS = [
        (480, 769),
        (979, 769)
        ]

def change_window(i):
    global WINDOW_ORIGIN, WINDOW_RIGHTTOP
    print "change window:", i

    WINDOW_ORIGIN = WINDOW_ORIGINS[i]
    WINDOW_RIGHTTOP = (
            WINDOW_ORIGIN[0] + WINDOW_WIDTH,
            WINDOW_ORIGIN[1] - WINDOW_HEIGHT
            )



def screencapture(filename):
    if(sys.platform == "linux2"):
        os.system('gnome-screenshot -w -f {0}'.format(filename))
    else:
        os.system('screencapture -x {0} >/dev/null 2>&1'.format(filename))

def screencaptureTemp():
    screencapture('temp/temp.png')

def getCurrentImage():
    # returns the current image.
    screencaptureTemp()
    if(sys.platform == "linux2"):
        image = Image.open("temp/temp.png")
    else:
        image_temp = Image.open("temp/temp.png")
        window_box = (
                WINDOW_ORIGIN[0],
                WINDOW_ORIGIN[1] - WINDOW_HEIGHT,
                WINDOW_ORIGIN[0] + WINDOW_WIDTH,
                WINDOW_ORIGIN[1],
               ) 
        image = image_temp.crop(window_box)
    
    return image

def change_next_window():
    os.system('osascript {0}/change_window.scpt'.format(ROOT_DIR))

def change_next_next_window():
    os.system('osascript {0}/change_window2.scpt'.format(ROOT_DIR))

def showCurrentWindow():
    # show the current window.
    image = getCurrentImage()
    image.show()

def captureCurrentWindow():
    # save the current window at temp/current_window.png".
    image = getCurrentImage()
    image.save('temp/current_window.png')

def get_normalized_image(image):
    # returns the normalized image.
    if(ASPECT_RATIO[0] != 1.0 and ASPECT_RATIO[1] != 1.0):
        image = image.resize((
            int(image.size[0] / ASPECT_RATIO[0]),
            int(image.size[1] / ASPECT_RATIO[1])
            ))
    return image


