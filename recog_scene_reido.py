# -*- encoding: utf-8 -*-
import kdebug
from defines import ROOT_DIR
import recog
from kimage import calc_sim_b
from recog import extf_of_rgb
from recog import recognize
from kscreen import getCurrentImage
from kscreen import get_normalized_image
from PIL import Image
from recog_scene import dictionary_scene


# ・dictionary カテゴリーをkeyとした辞書. そのvalueは以下を持つ:
#   ・feature このカテゴリーのモデル特徴量
#   ・extf imageを引数として, その特徴量を返す関数
#   ・scan_box 走査範囲. ない場合はrec_boxと同じ値が使われる
#   ・rec_box このカテゴリーを判別する矩形領域
#   ・preprocess imageを引数として, その前処理をした画像を返す関数
scene_reido_dictionary = dict()
#for k, v in dictionary_scene.items():
#    scene_reido_dictionary[k] = v

scene_reido_dictionary["start"] = {
        "rec_box": (303, 19, 304, 20),
        "scan_box": (302, 18, 305, 21),
        "feature": (255, 0, 0),
        "extf": extf_of_rgb,
        }
scene_reido_dictionary["yes_1"] = {
        "rec_box": (180, 274, 181, 275),
        "scan_box": (179, 273, 182, 276),
        "feature": (255, 0, 0),
        "extf": extf_of_rgb,
        }
scene_reido_dictionary["chat_hello"] = {
        "rec_box": (104, 203, 105, 204),
        "scan_box": (103, 202, 104, 205),
        "feature": (34, 131, 0),
        "extf": extf_of_rgb,
        }
ok_1 = {
        "rec_box": (247, 271, 248, 272),
        "scan_box": (246, 270, 249, 273),
        "feature": (255, 0, 0),
        "extf": extf_of_rgb,
        }
scene_reido_dictionary["ok_1"] = ok_1
scene_reido_dictionary["ok_2"] = {
        "rec_box": (249, 231, 250, 232),
        "scan_box": (248, 230, 251, 233),
        "feature": (255, 0, 0),
        "extf": extf_of_rgb,
        }
scene_reido_dictionary["retry"] = {
        "rec_box": (194, 54, 195, 55),
        "scan_box": (193, 53, 196, 56),
        "feature": (255, 0, 0),
        "extf": extf_of_rgb,
        }
#scene_reido_dictionary["yes_2"] = {
#        "rec_box": (171, 268, 172, 269),
#        "scan_box": (171, 268, 172, 269),
#        "feature": (255, 0, 0),
#        "extf": extf_of_rgb,
#        "preprocess": lambda x: x
#        }
scene_reido_dictionary["end_ok"] = {
        "rec_box": (246, 178, 247, 179),
        "feature": (255, 17, 17),
        "extf": extf_of_rgb,
        }

ans_select_dictionary = {}
ans_select_dictionary["4"] = {
        "rec_box": (87, 92, 88, 93),
        "feature": (255, 20, 20),
        "extf": extf_of_rgb,
        }
ans_select_dictionary["3"] = {
        "rec_box": (87, 155, 88, 156),
        "feature": (255, 20, 20),
        "extf": extf_of_rgb,
        }
ans_select_dictionary["2"] = {
        "rec_box": (87, 218, 88, 219),
        "feature": (255, 20, 20),
        "extf": extf_of_rgb,
        }
ans_select_dictionary["1"] = {
        "rec_box": (87, 281, 88, 282),
        "feature": (255, 20, 20),
        "extf": extf_of_rgb,
        }


is_nonbattle_mode_dictionary = {}
is_nonbattle_mode_dictionary["is_nonbattle"] = ok_1

def judge_reido_scene(image = None):
    """
    戦闘・非戦闘状態関係なくレイドの場面を判断する.
    """
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    non_key, non_sim = recognize(
            image,
            recog.match_rgb,
            0.80,
            scene_reido_dictionary
            )
    non_sim = non_sim * 0.75 / 0.80

    battle_key, battle_sim = recog.recognize(
            input_image = image,
            match = calc_sim_b,
            threshold = 0.75,
            dictionary = dictionary_scene
            )
    if(battle_sim >= non_sim):
        return battle_key
    return non_key

def judge_non_battle_scene(image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key, sim = recognize(
            image,
            recog.match_rgb,
            0.82,
            scene_reido_dictionary
            )
    return key

def judge_is_non_battle_scene(image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key, sim = recognize(
            image,
            recog.match_rgb,
            0.84,
            is_nonbattle_mode_dictionary
            )
    if(key == None):
        return False
    return key == "is_nonbattle"

def judge_ans_num(image = None):
    if(image == None):
        image = getCurrentImage()
        image = get_normalized_image(image)

    key, sim = recognize(
            image,
            recog.match_rgb,
            0.76,
            ans_select_dictionary
            )
    return key

#image = Image.open("temp/temp.png")
#print judge_non_battle_scene(image)
