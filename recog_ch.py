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

def cut_and_recog_char(image, SIZE=CH_SIZE):
    # 切り出しと同時に文字認識を行う.
    # 候補文字から最大の文字を選択することで半角、全角を認識できる.
    # SIZEは使わない

    def cut_horizontally(h_range):
        # d のピクセルは含めるが
        # u のピクセルは含めるない
        u = -1 
        d = 0
        is_white_prev = False

        for j in range(image.size[1]-1):
            if(u == -1):
                # 横ラインが白ならばupperをjにする
                if(not is_hline_range(image, j, 0, h_range)):
                    u = j
                    is_white_prev = True
            else:
                if(is_hline_range(image, j, 0, h_range)):
                    # 前回が白のときだけdownを更新する
                    if(is_white_prev):
                        d = j
                    is_white_prev = False
                else:
                    is_white_prev = True
        if(not is_hline_range(image, j + 1, 0, h_range)):
            d = j + 1
        return d, u

    def get_max_sim_index(candidates):
        max_sim = -1000
        max_i = -1
        for i, c in enumerate(candidates):
            if(c["sim"] > max_sim):
                max_sim = c["sim"]
                max_i = i
        return max_i

    def get_candidate(l, r, now_l):
        d, u = cut_horizontally((l, r))
        ch_image = image.crop([l, u, r, d])
        ch_dir = kchar.get_ch_dir_where((r-l, d-u), 4)
        ch, sim = to_char(ch_image, ch_dir)

        # for debug
#        print "get candidate:"
#        print "\tleft donw:", (l, d)
#        print "\tsize:", (r-l, d-u)
#        print u"\tch: ", ch if ch != None else ""
#        print
        
        return {"value": ch, "sim": sim, "img": ch_image, "left": now_l}

    # 縦方向の切り出し
    l = -1 
    i = 0

    # 文字候補
    candidates = []

    # 結果
    ret_imgs = []
    ret_chars = u""
    sims = []

    while(i < image.size[0]):
        if(l == -1):
            # 縦ラインが白ならばleftをiにする
            if(not is_vline(image, i, 0)):
                l = i
        else:
            # 縦ラインが黒(背景)ならcutする
            if(is_vline(image, i, 0)):
                r = i

                if(len(candidates) == 0):
                    candidates.append(get_candidate(l, r, l))
                else:
                    width = r - candidates[0]["left"]

                    # width が23以上になった場合は、そこまでの候補文字から
                    # 類似度が最も高い候補文字を選択する
                    if(width >= 23):
#                        print("width >= 23")
                        max_i = get_max_sim_index(candidates)

                        c = candidates[max_i]
                        if(c["value"] == None):
                            ret_chars += u"　"
#                            print u"append ret:'{0}'".format(u"　")
                        else:
                            ret_chars += c["value"]
#                            print u"append ret:'{0}'".format(c["value"])
                        sims.append(c["sim"])
                        ret_imgs.append(c["img"])

                        if(len(candidates) == max_i + 1):
                            candidates = []
                            candidates.append(get_candidate(l, r, l))
                        else:
                            i = candidates[max_i + 1]["left"] - 1
                            candidates = []
#                            candidates.append(get_candidate(candidates[0]["left"], r, l))
                    else:
                        candidates.append(get_candidate(candidates[0]["left"], r, l))
                l = -1 
        i += 1

#    print "check candidate"
    while(len(candidates) > 0):
#        print len(candidates)
        
        max_i = get_max_sim_index(candidates)
#        print max_i
        c = candidates[max_i]
        if(c["value"] == None):
            ret_chars += u"　"
#            print u"append ret:'{0}'".format(u"　")
        else:
            ret_chars += c["value"]
#            print u"append ret:'{0}'".format(c["value"])
        sims.append(c["sim"])
        ret_imgs.append(c["img"])
        candidates = candidates[max_i+1:]

    return ret_chars, ret_imgs, sims

def cut_char_all(image, SIZE=CH_SIZE):
    ret = []
    
    def cut_horizontally(h_range):
        # d のピクセルは含めるが
        # u のピクセルは含めるない
        u = -1 
        d = 0
        is_white_prev = False

        for j in range(image.size[1]-1):
            if(u == -1):
                # 横ラインが白ならばupperをjにする
                if(not is_hline_range(image, j, 0, h_range)):
                    u = j
                    is_white_prev = True
            else:
                if(is_hline_range(image, j, 0, h_range)):
                    # 前回が白のときだけdownを更新する
                    if(is_white_prev):
                        d = j
                    is_white_prev = False
                else:
                    is_white_prev = True
        if(not is_hline_range(image, j + 1, 0, h_range)):
            d = j + 1
        return d, u

    # 縦方向の切り出し
    l = -1 
    r = 0
    m = 0
    i = 0
    while(i < image.size[0]):
        if(l == -1):
            # 縦ラインが白ならばleftをiにする
            if(not is_vline(image, i, 0)):
                l = i
        else:
            # 縦ラインが黒(背景)ならcutする
            if(is_vline(image, i, 0)):
                r = i
                d, u = cut_horizontally((l, r))
                ret.append(image.crop([l, u, r, d]))
                l = -1 
        i += 1
    return ret

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


def to_char(image, ch_dir = kchar.CH_DIR):
    image = image.resize((CH_SIZE,CH_SIZE))
    barray1 = g_to_barray(image.getdata())

    max_sim = -1
    max_key = None

    for key, value in ch_dir.items():
        sim = calc_sim_b(barray1, value)
        if(sim > max_sim):
            max_sim = sim
            max_key = key
    return max_key, max_sim


# 問題文の文字を認識する
def to_chars_question(image):
    gimages = screen_to_boximg(image, CONTENT_BOXES, rgb_to_barray_near_white)
    chars = u""
    imgs = []
    sims = []

    for img in gimages:
        chars2, imgs2, sims2 = cut_and_recog_char(img, CH_SIZE)
        chars += chars2
        imgs += imgs2
        sims += sims2

    return chars, imgs, sims

def to_chars_choice(image, i):
    img = screen_to_boximg(image, CHOICE_BOXES[i], rgb_to_barray_near_black_reverse)
    chars = u""
    imgs = []
    sims = []

    chars2, imgs2, sims2 = cut_and_recog_char(img, CHOICE_CH_SIZE)
    chars += chars2
    imgs += imgs2
    sims += sims2
    return chars, imgs, sims

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
        ch, sim = to_char(img)
        chars.append(ch)
    return kchar.list_to_str_unicode(chars), imgs


# running code ----------------------------------------------

#image = Image.open("temp/ques/1680.png")
#img = screen_to_boximg(image, CHOICE_BOX2, rgb_to_barray_near_black_reverse)
#chars, imgs, sims = to_chars_question(image)
#chars, imgs, sims = to_chars_choice(image, 3)
#image = screen_to_boximg(image, CONTENT_BOX, rgb_to_barray_near_white)

#image = screen_to_boximg(image, CONTENT_BOX_2, rgb_to_barray_near_white)
#chars, imgs, sims = cut_and_recog_char(image)

#print chars
#print sims
#for i, im in enumerate(ch_imgs):
#    im.save("temp/temp_char/{0}.png".format(i))
