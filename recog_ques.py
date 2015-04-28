# -*- encoding: utf-8 -*-
# 問題認識
import kdebug
import os
import os.path
import kchar

from klogger import logger
from PIL import Image
from kimage import *
from kmouse import *
from kscreen import *
from kfile import *
from recog_ch import *
from ktext import calc_sim_text

from kques import QUESES
from kques import show_question
import time

GENRE = [
        u"理系",
        u"生活＆雑学",
        u"芸能",
        u"スポーツ",
        u"文系",
        u"アニメ＆ゲーム",
        ]

def get_questions_where(genre, panel=None, lrange=None):
    ret = []
    for value in QUESES:
        if(value["type"] != 0):
            continue
        if(genre != None and value["genre"] != genre):
            continue
        if(panel != None and value["panel"] != panel):
            continue
        if(lrange != None):
            if(len(value["question"]) < lrange[0]
                or len(value["question"]) > lrange[1]):
                continue
        ret.append(value)
    return ret

def recog_question(s, queses):
    max_q = None
    max_sim = -1

    for q in queses:
        s2 = q["question"]
        sim = calc_sim_text(s, s2)
        if(sim > max_sim):
            max_sim = sim
            max_q = q

    return max_q, max_sim


def to_genre_char(image):
    image = image.resize((GENRE_CH_SIZE,GENRE_CH_SIZE))
    barray1 = g_to_barray(image.getdata())
    
    max_sim = -1
    max_key = None

    for key, value in kchar.genre_items_all():
        sim = calc_sim_b(barray1, value)
        if(sim > max_sim):
            max_sim = sim
            max_key = key
    return max_key

def recog_genre(image):
    gimages = screen_to_boximg(image, GENRE_BOX,rgb_to_barray_near_white)
    gimgs = cut_char_zenkaku(gimages, GENRE_CH_SIZE)

    s = u""
    for gimg in gimgs:
        s += to_genre_char(gimg)
    print s

    max_q = None
    max_sim = -1

    for q in GENRE:
        sim = calc_sim_text(s, q, 0)
        if(sim > max_sim):
            max_sim = sim
            max_q = q
    return max_q, max_sim

def recog_choice(choices, q):
    max_q = None
    max_sim = -1
    

    for i, s in enumerate(choices):
        # for debu
        ns = u""
        for ch in s:
            ns += ch

        sim = calc_sim_text(ns, q["answer"])
        print u"{0}: {1}-{2}".format(sim, ns, q["answer"])
        if(sim > max_sim):
            max_sim = sim
            max_q = i
    return max_q, max_sim

#image_su =  Image.open("charimg/30B9.png")
#image_su.show()
#
#save_ch_img(u"ス", image_su)

def get_choices(image):
    """
    Returns the unicode characters of choices from screenshot image.
    @param image a screenshot image
    """

    choices = []
    for i in range(4):
        cchars, cimgs = to_chars(
                image,
                cut_char_zenkaku,
                CHOICE_BOXES[i],
                CHOICE_CH_SIZE,
                rgb_to_barray_near_black_reverse
                )
        print(cchars)
        choices.append(cchars)
    return choices

def get_answer(image, q, choices = None):
    """
    Returns the index of the answer of the quetion.
    @param image a screenshot image
    @q  the question
    @choices the unicode characters of choices (Default: None)
    """

    if(choices == None):
        choices = get_choices(image)

    choice_index, csim = recog_choice(choices, q)
    print "Answer:", q["answer"]
    print "Select:", choice_index+1
    return choice_index

def get_genre(image):
    genre, gsim = recog_genre(image)
    return genre

def get_ques(image, genre, panel = None):
    chars, imgs = to_chars(image, cut_char_zenkaku)
    slen = len(chars)

    queses = get_questions_where(genre, panel, (slen - 2, slen + 2))
    q, sim = recog_question(chars, queses)

    qcontent = kchar.list_to_str_unicode(chars)
    return q,sim,qcontent

def recog_test(num, panel=None):
    path = "temp/ques/{0}.png".format(num)
    if(not os.path.exists(path)):
        return
    print path
    image =  Image.open(path)
    image.show()

    genre, sim = recog_genre(image)
    print genre

    chars, imgs = to_chars(image, cut_char_zenkaku)
    print chars

    slen = len(chars)
    queses = get_questions_where(genre, panel, (slen - 2, slen + 2))

    stime = time.clock()
    q, sim = recog_question(chars, queses)
    etime = time.clock()
    print etime - stime, "s"

    print q["question"]
    print sim
    print "{0} == {1}?".format(len(chars), len(q["question"]))
    if(sim > 0.5):
        choices = []
        for i in range(4):
            cchars, cimgs = to_chars(
                    image,
                    cut_char_zenkaku,
                    CHOICE_BOXES[i],
                    CHOICE_CH_SIZE,
                    rgb_to_barray_near_black_reverse
                    )
            print(cchars)
            choices.append(cchars)
        choice_index, csim = recog_choice(choices, q)
        print "Answer:", q["answer"]
        print "Select:", choice_index+1


#recog_test(566, u"1色")
#recog_test(566)
