# -*- encoding: utf-8 -*-
import kdebug
from kimage import *
from kiso import *
from defines import ROOT_DIR
import recog
from kscreen import getCurrentImage
from kscreen import ASPECT_RATIO
from kscreen import get_normalized_image

IS_GENRE_IMG_PATH = ROOT_DIR + "/res/is_genre.png"
IS_QUES_IMG_PATH = ROOT_DIR + "/res/is_question.png"
IS_STAGE_SELECT_IMG_PATH = ROOT_DIR + "/res/is_stage_select.png"


# ・dictionary カテゴリーをkeyとした辞書. そのvalueは以下を持つ:
#   ・feature このカテゴリーのモデル特徴量
#   ・extf imageを引数として, その特徴量を返す関数
#   ・scan_box 走査範囲. ない場合はrec_boxと同じ値が使われる
#   ・rec_box このカテゴリーを判別する矩形領域
#   ・preprocess imageを引数として, その前処理をした画像を返す関数
dictionary_scene = dict()
dictionary_scene["is_genre"] = {
        "rec_box": (34, 162, 226, 270),
        "feature": recog.extf_of_is_genre(Image.open(IS_GENRE_IMG_PATH)),
        "extf": recog.extf_of_is_genre,
        "preprocess": lambda x: barray_to_gimage(rgb_to_barray_near_black(x.getdata()), x.size)
        }
dictionary_scene["is_question"] = {
        "rec_box": (13, 278, 70, 435),
        "scan_box": getSurroundBox((13, 278, 70, 435), 1),
        "feature": recog.extf_of_is_question(Image.open(IS_QUES_IMG_PATH)),
        "extf": recog.extf_of_is_question,
        "preprocess": lambda x: barray_to_gimage(g_to_barray(rgb_to_garray_average(x.getdata())), x.size)
        }
dictionary_scene["is_stage_select"] = {
        "rec_box": (27, 187, 39, 200),
        "scan_box": getSurroundBox((27, 187, 39, 200), 1),
        "feature": g_to_barray(Image.open(IS_STAGE_SELECT_IMG_PATH).getdata()),
        "extf": lambda x: g_to_barray(x.getdata()),
        "preprocess": lambda x: barray_to_gimage(g_to_barray(rgb_to_garray_average(x.getdata())), x.size)
        }


# 正誤の判別に利用する辞書
erratum_dictionary = dict()
erratum_dictionary["is_seikai"] = {
        "rec_box": (165, 504, 169, 508),
        "scan_box": (165, 504, 169, 508),
        "feature": 0,
        "extf": recog.extf_of_answer_erratum,
        "preprocess": lambda x: x
        }
erratum_dictionary["is_hazure"] = {
        "rec_box": (165, 504, 169, 508),
        "scan_box": (165, 504, 169, 508),
        "feature": 255,
        "extf": recog.extf_of_answer_erratum,
        "preprocess": lambda x: x
        }

# 4択問題の答えの数字を判別に利用する辞書
ansnum_rec = (62, 65, 68, 70)
ansnum_dictionary = dict()
ansnum_dictionary["num1"] = {
        "rec_box": ansnum_rec,
        "scan_box": ansnum_rec,
        "feature": (180, 47, 187),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
ansnum_dictionary["num2"] = {
        "rec_box": ansnum_rec,
        "scan_box": ansnum_rec,
        "feature": (68, 157, 128),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
ansnum_dictionary["num3"] = {
        "rec_box": ansnum_rec,
        "scan_box": ansnum_rec,
        "feature": (125, 152, 195),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
ansnum_dictionary["num4"] = {
        "rec_box": ansnum_rec,
        "scan_box": ansnum_rec,
        "feature": (234, 102, 22),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }

# 色で判別するシーン
scene_color_dictionary = dict()
scene_color_dictionary["skip"] = {
        "rec_box": (340, 697, 346, 702),
        "scan_box": (340, 697, 346, 702),
        "feature": (104, 189, 98),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
scene_color_dictionary["skip_yes"] = {
        "rec_box": (175, 251, 183, 258),
        "scan_box": (175, 251, 183, 258),
        "feature": (255, 39, 39),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
scene_color_dictionary["end_ok"] = {
        "rec_box": (207, 154, 242, 157),
        "scan_box": (207, 154, 242, 157),
        "feature": (255, 6, 6),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
scene_color_dictionary["follow_no"] = {
        "rec_box": (324, 273, 332, 280),
        "scan_box": (324, 273, 332, 280),
        "feature": (35, 186, 255),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }
scene_color_dictionary["subque_compelete"] = {
        "rec_box": (246, 274, 256, 279),
        "scan_box": (246, 274, 256, 279),
        "feature": (255, 37, 37),
        "extf": recog.extf_of_rgb,
        "preprocess": lambda x: x
        }



# is_genreに使われる画像のキャプチャ
# window sizeがorigin sizeであることが必要
#def capture_is_genre():
#    image = getCurrentImage()
#    barray_nearblack = imagetool.toBinaryArrayNearBlackFromRGBArray(image.getdata())
#    image_nearblack = imagetool.toGrayScaleImageFromBinaryArray(barray_nearblack, image.size)
#    rec_box = dictionary_scene["is_genre"]["rec_box"]
#    prep = dictionary_scene["is_genre"]["preprocess"]
#
#    image = imagetool.crop(rec_box, image_nearblack)
#    prep(image)
#    recog.remove_isolate_point(image, 255, 0)
#    return image

# window sizeがorigin sizeであることが必要
#def capture_is_stage_select():
#    image = getCurrentImage()
#    array = imagetool.toGrayScaleArrayWithAverageFromRGBArray(image.getdata())
#    barray = imagetool.toBinaryArrayFromGrayScaleArray(array)
#    image = imagetool.toGrayScaleImageFromBinaryArray(barray, image.size)
#    image.show()
#
#    rec_box = dictionary_scene["is_stage_select"]["rec_box"]
#    image = imagetool.crop(rec_box, image)
#    return image

#def capture_is_question():
#    image = getCurrentImage()
#    array = imagetool.toGrayScaleArrayWithAverageFromRGBArray(image.getdata())
#    barray = imagetool.toBinaryArrayFromGrayScaleArray(array)
#    image = imagetool.toGrayScaleImageFromBinaryArray(barray, image.size)
#
#    rec_box = dictionary_scene["is_question"]["rec_box"]
#    image = imagetool.crop(rec_box, image)
#    return image


def judge_scene(image = None):
    # クエスト時における現在の状態を判別する
    # ジャンル選択、問題、などがある.
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key = recog.recognize(
            input_image = image,
            match = calc_sim_b,
            threshold = 0.8,
            dictionary = dictionary_scene
            )
    return key

def judge_erratum(image = None):
    # 正解か不正解かを判定する.
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key = recog.recognize(
            image,
            recog.match_answer_erratum,
            0.0,
            erratum_dictionary
            )
    return key

def judge_ansnum(image = None):
    # 問題の答えを画像から判定する.
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key = recog.recognize(
            image,
            recog.match_rgb,
            0.0,
            ansnum_dictionary
            )
    if(key == None):
        return -1
    if(key == "num1"):
        return 1
    if(key == "num2"):
        return 2
    if(key == "num3"):
        return 3
    if(key == "num4"):
        return 4
    return -1

def judge_scene_color(image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key = recog.recognize(
            image,
            recog.match_rgb,
            0.92,
            scene_color_dictionary
            )
    return key


