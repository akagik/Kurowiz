# -*- encoding: utf-8 -*-
import kdebug
from kimage import *
from PIL import Image
from klogger import logger
from kiso import inBox

def prep_is_genre(image):
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if(inBox((x, image.size[1] - y - 1), (93, 9, 178, 95))):
                image.putpixel((x,y), 255)

# image はグレースケールとする
def extf_of_is_genre(image):
    f = []
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if(not inBox((x, image.size[1] - y - 1), (93, 9, 178, 95))):
                f.append(0 if image.getpixel((x, y)) == 0 else 1)
    return f


# image はグレースケールとする
def extf_of_is_question(image):
    f = []
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if(not inBox((x, image.size[1] - y - 1), (14, 7, 50, 111))):
                f.append(0 if image.getpixel((x, y)) == 0 else 1)
    return f

# image はRGBとする
# 特徴量は平均したRの値
def extf_of_answer_erratum(image):
    r = 0
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r += image.getpixel((x, y))[0]
    return r / (image.size[0] * image.size[1])

# image はRGBとする
# 特徴量は平均したRGBの値
def extf_of_rgb(image):
    r = 0
    g = 0
    b = 0
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            p = image.getpixel((x, y))
            r += p[0]
            g += p[1]
            b += p[2]
    length = (image.size[0] * image.size[1])
    return (r / length, g / length, b / length) 

def match_answer_erratum(f1, f2):
    return abs(f1 - f2) / 255.0

def match_rgb(f1, f2):
    return (255 * 3 - (abs(f1[0] - f2[0]) + abs(f1[1] - f2[1]) +  abs(f1[2] - f2[2]))) / (255.0 * 3)

# black_valueを黒点, white_valueを白点の値として, 孤立した黒点を
# 白点に変える
#def remove_isolate_point(image, white_value, black_value):
#    for y in range(image.size[1]):
#        for x in range(image.size[0]):
#            if(imagetool.is_isolate_point((x,y), image, black_value)):
#                image.putpixel((x, y), white_value)

# 画像認識をする.
# 返り値は最も近いカテゴリー. どのカテゴリーにも属さない場合はNoneを返す.
#
# ・input_image 入力画像
# ・match 比較したい2つの特徴量を比較して, その類似度を返す関数
# ・threshold 類似度の閾値
# ・dictionary カテゴリーをkeyとした辞書. そのvalueは以下を持つ:
#   ・feature このカテゴリーのモデル特徴量
#   ・extf imageを引数として, その特徴量を返す関数
#   ・scan_box 走査範囲. ない場合はrec_boxと同じ値が使われる
#   ・rec_box このカテゴリーを判別する矩形領域
#   ・preprocess imageを引数として, その前処理をした画像を返す関数, なければ何もしない
def recognize(input_image, match, threshold, dictionary):
    category_key = None
    category_max_sim = -1
    category_max_image = None # for debug

    for key, value in dictionary.items():
        rec_box = value["rec_box"]
        if "scan_box" in value:
            scan_box = value["scan_box"]
        else:
            scan_box = rec_box

        rec_width = rec_box[2] - rec_box[0]
        rec_height = rec_box[3] - rec_box[1]

        if "preprocess" in value:
            prep_image = value["preprocess"](input_image)
        else:
            prep_image = input_image
        
        max_sim = -1
        for x in range(scan_box[0], scan_box[2] - rec_width + 1):
            for y in range(scan_box[1], scan_box[3] - rec_height + 1):
                comp_box = (x, y, x + rec_width, y + rec_height)
                comp_image = crop_box_left_down(comp_box, prep_image)
                comp_feature = value["extf"](comp_image)

                # for debug
#                if(key == "subque_compelete"):
#                    logger.debug("f:{0}".format(comp_feature))

                sim = match(value["feature"], comp_feature)
#                print x, ",", y, ":", sim
                if(sim > max_sim):
                    max_sim = sim
                    category_max_image = comp_image

        if(max_sim > category_max_sim):
            category_max_sim = max_sim
            category_key = key
#        logger.debug("{0} -> sim: {1}".format(key, max_sim))

    if(category_max_sim < threshold):
        return None, -1

    return category_key, max_sim
