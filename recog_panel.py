# -*- encoding: utf-8 -*-
import kdebug
from kimage import *
from kiso import *
from defines import ROOT_DIR
import recog
from kscreen import getCurrentImage
from kscreen import ASPECT_RATIO
from kscreen import get_normalized_image


# ・dictionary カテゴリーをkeyとした辞書. そのvalueは以下を持つ:
#   ・feature このカテゴリーのモデル特徴量
#   ・extf imageを引数として, その特徴量を返す関数
#   ・scan_box 走査範囲. ない場合はrec_boxと同じ値が使われる
#   ・rec_box このカテゴリーを判別する矩形領域
#   ・preprocess imageを引数として, その前処理をした画像を返す関数
# rec_box は右上の点は含めない

# パネル色認識
panel_rec_rects = [
        [22, 61, 23, 62],
        [78, 59, 79, 60],
        [51, 24, 52, 25],
        ]

panel_dictionaries = []
for i, rec in enumerate(panel_rec_rects):
    panel_dict = dict()
    panel_dict["red"] = {
            "rec_box": rec,
            "feature": (255, 0, 0),
            "extf": recog.extf_of_rgb,
            }
    panel_dict["yellow"] = {
            "rec_box": rec,
            "feature": (255, 255, 0),
            "extf": recog.extf_of_rgb,
            }
    panel_dict["blue"] = {
            "rec_box": rec,
            "feature": (0, 0, 255),
            "extf": recog.extf_of_rgb,
            }
    panel_dictionaries.append(panel_dict)

# 0: 左上のパネル
# 1: 右上のパネル
# 2: 左下のパネル
# 3: 右下のパネル
panel_rects = [
        [34, 162, 225, 268],
        [222, 162, 413, 268],
        [34, 37, 225, 143],
        [222, 37, 413, 143],
        ]


# numは
# 0: 左上のパネル
# 1: 右上のパネル
# 2: 左下のパネル
# 3: 右下のパネル
def judge_panel_color(num, image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)
    
    image = crop_box_left_down(panel_rects[num], image)

    is_red = False
    is_blue = False
    is_yellow = False

    for i, dic in enumerate(panel_dictionaries):
        key = recog.recognize(
                image,
                recog.match_rgb,
                0.0,
                dic
                )
        if(key == "red"):
            is_red = True
        elif(key == "yellow"):
            is_yellow = True
        elif(key == "blue"):
            is_blue = True
    color_size = 0
    if(is_red):
        color_size += 1
    if(is_yellow):
        color_size += 1
    if(is_blue):
        color_size += 1

    return color_size, (1 if is_red else 0, 1 if is_yellow else 0, 1 if is_blue else 0)

def judge_panels(image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)
    
    ret = [None] * 4
    for i in range(len(ret)):
        ret[i] = judge_panel_color(i, image)

    return ret

