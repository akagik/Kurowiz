# -*- encoding: utf-8 -*-
# 文字認識の関数をまとめファイル
import kdebug
from klogger import logger
from PIL import Image
from kimage import *
from kscreen import *
import kchar


# 問題画面における各特徴の矩形領域を定義

# ジャンルの矩形領域とその文字の大きさ
GENRE_BOX = (70,296, 181, 317)
GENRE_CH_SIZE = 15

# 問題文の矩形領域とその文字の大きさ
CONTENT_BOX = (42,386, 395, 410)
CONTENT_SIZE = (
        CONTENT_BOX[2] - CONTENT_BOX[0],
        CONTENT_BOX[3] - CONTENT_BOX[1],
        )
CONTENT_BOX_2 = (42,361, 395, 361 + CONTENT_SIZE[1])
CONTENT_BOX_3 = (42,337, 395, 337 + CONTENT_SIZE[1])
CONTENT_BOXES = [
        CONTENT_BOX,
        CONTENT_BOX_2,
        CONTENT_BOX_3,
        ]
CH_SIZE = 20

# 選択肢の矩形領域とその文字の大きさ
CHOICE_BOX1 = (95, 237, 380, 237 + 25)
CHOICE_BOX2 = (95, 173, 380, 173 + 25)
CHOICE_BOX3 = (95, 111, 380, 111 + 25)
CHOICE_BOX4 = (95,  47, 380,  47 + 25)
CHOICE_BOXES = [
        CHOICE_BOX1,
        CHOICE_BOX2,
        CHOICE_BOX3,
        CHOICE_BOX4,
        ]
CHOICE_CH_SIZE = 20



def next_white_i(image, start):
    for i in range(start, image.size[0]):
        if(not is_vline(image, i, 0)):
            return i
    return -1

def cut_char_zenkaku(image, SIZE=CH_SIZE):
    ret = []

    # 縦方向の切り出し
    l = -1 
    r = 0
    m = 0
    is_slim = False
    i = 0
    while(i < image.size[0]):
        if(l == -1):
            if(not is_vline(image, i, 0)):
                l = i
        else:
            if(is_vline(image, i, 0)):
                if(not is_slim):
                    r = i
                    # 通常より小さいとき
                    if(r-l <= SIZE - 4):
                        # 次に列も白のときは無視
                        if(i + 1 < image.size[0] and not is_vline(image, i+1, 0)):
                            i += 1
                            continue
                        r = i
                        i = next_white_i(image, i+1)
                        if(i == -1):
                            image_char = crop_box_left_down(
                                    (l,
                                     0,
                                     r,
                                     image.size[1]), image)
                            ret.append(image_char)
                            break
                        else:
                            m = i
                            is_slim = True
                    # 通常通りの大きさのとき
                    else:
                        image_char = crop_box_left_down(
                                (l,
                                 0,
                                 r,
                                 image.size[1]), image)
                        l = -1 
                        ret.append(image_char)
                else:
                    w = i - l 
                    if(w < SIZE - 4):
                        pass
                    # 16 ~ 21のとき
                    elif(w <=SIZE + 1):
                        image_char = crop_box_left_down(
                                (l,
                                 0,
                                 i,
                                 image.size[1]), image)
                        l = -1
                        ret.append(image_char)
                        is_slim = False
                    # 22~のとき
                    else:
                        image_char = crop_box_left_down(
                                (l,
                                 0,
                                 r,
                                 image.size[1]), image)
                        l = m
                        i = m 
                        ret.append(image_char)
                        is_slim = False
        i += 1

    # 横方向の切り出し
    for index in range(len(ret)):
        ch_img = ret[index]
        u = -1 
        d = 0
        is_white_prev = False

        for j in range(ch_img.size[1]-1):
            if(u == -1):
                if(not is_hline(ch_img, j, 0)):
                    u = j
                    is_white_prev = True
            else:
                if(is_hline(ch_img, j, 0)):
                    if(is_white_prev):
                        d = j
                    is_white_prev = False
                else:
                    is_white_prev = True
        if(not is_hline(ch_img, j + 1, 0)):
            d = j + 1
        image_char = ch_img.crop((0, u, ch_img.size[0], d))
        ret[index] = image_char
    return ret



def screen_to_boximg(image, boxes, rgb_to_barray):
    if(type(boxes) == type([])):
        ret = []
        for b in boxes:
            image_content = crop_box_left_down(b, image)
            barray = rgb_to_barray(image_content.getdata())
            ret.append(barray_to_gimage(barray, image_content.size))
        return ret
    else:
        image_content = crop_box_left_down(boxes, image)
        barray = rgb_to_barray(image_content.getdata())
    return barray_to_gimage(barray, image_content.size)


def to_char(image):
    image = image.resize((CH_SIZE,CH_SIZE))
    barray1 = g_to_barray(image.getdata())

    max_sim = -1
    max_key = None

    for key, value in kchar.items_all():
        sim = calc_sim_b(barray1, value)
        if(sim > max_sim):
            max_sim = sim
            max_key = key
    return max_key

def to_chars(
        image,
        cut_method,
        boxes = CONTENT_BOXES,
        SIZE=CH_SIZE,
        rgb_to_barray = rgb_to_barray_near_white
        ):
    gimages = screen_to_boximg(image, boxes, rgb_to_barray)

    chars = []

    imgs = []
    if(type(gimages) == type([])):
        for img in gimages:
            imgs += cut_method(img, SIZE)
    else:
        imgs += cut_method(gimages, SIZE)

    for img in imgs:
        chars.append(to_char(img))
    return kchar.list_to_str_unicode(chars), imgs


# running code ----------------------------------------------

#image = Image.open("1639.png")
#image.show()
#string, imgs = to_chars(
#        image,
#        cut_char_zenkaku
#        )
#print string
