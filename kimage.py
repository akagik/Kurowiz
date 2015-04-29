# -*- coding: utf-8 -*-
import kdebug
from PIL import Image

def g_to_barray(gsarray):
    return list(map(lambda x: 0 if x < 128 else 1, gsarray))

def b_to_garray(barray):
    return list(map(lambda x: 0 if x == 0 else 255, barray))

def barray_to_gimage(bdata, size):
    image = Image.new("L", size)
    image.putdata(b_to_garray(bdata))
    return image

def rgb_to_barray_near_black(px):
    px2 = []
    for data in px:
        if(data[0] < 128 and data[1] < 128 and data[2] < 128):
            px2.append(0)
        else:
            px2.append(1)
    return px2

def rgb_to_barray_near_black_reverse(px):
    px2 = []
    for data in px:
        if(data[0] < 128 and data[1] < 128 and data[2] < 128):
            px2.append(1)
        else:
            px2.append(0)
    return px2

def rgb_to_garray_average(px):
    px2 = []
    for data in px:
        px2.append((data[0] + data[1] + data[2]) / 3)
    return px2

def rgb_to_barray_near_white(px):
    px2 = []
    for data in px:
        if(data[0] >= 128 and data[1] >= 128 and data[2] >= 128):
            px2.append(1)
        else:
            px2.append(0)
    return px2

def rgb_to_barray_near_white150(px):
    px2 = []
    for data in px:
        if(data[0] >= 150 and data[1] >= 150 and data[2] >= 150):
            px2.append(1)
        else:
            px2.append(0)
    return px2


def crop_box_left_down(box, image):
    # This function is the same as Image.crop except for the origin is left down.
    iheight = image.size[1]
    box2 = (
            int(box[0]),
            int(iheight - box[3]),
            int(box[2]),
            int(iheight - box[1])
            )
#    print "crop box:", box2
    return image.crop(box2)

def calc_sim_b(bdata1, bdata2):
    if(len(bdata1) != len(bdata2)):
        print "Error : bdata1 length does not match bdata2 length.",\
            "len(bdata1):", len(bdata1), ", len(bdata2):", len(bdata2) 
        return -1

    count = 0
    length = len(bdata1)
    for i in range(length):
        if(bdata1[i] == bdata2[i]):
            count += 1

    return float(count) / length


def is_vline(image, i, color):
    # returns True if the value of pixel at the column i line of the image is the color.
    for j in range(image.size[1]):
        if(image.getpixel((i, j)) != color):
            return False
    return True

def is_vline_range(image, i, color, ran):
    for j in range(ran[0], ran[1]):
        if(image.getpixel((i, j)) != color):
            return False
    return True

def is_hline(image, j, color):
    # returns True if the value of pixel at the row j line of the image is the color.
    for i in range(image.size[0]):
        if(image.getpixel((i, j)) != color):
            return False
    return True

def is_hline_range(image, j, color, ran):
    for i in range(ran[0], ran[1]):
        if(image.getpixel((i, j)) != color):
            return False
    return True

def count_color(barray, color):
    # returns the size of the element whose value is color.
    # barray array
    # color
    count = 0
    for b in barray:
        if(b == color):
            count += 1
    return count
