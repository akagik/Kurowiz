# -*- encoding: utf-8 -*-
import kdebug
from klogger import logger
from PIL import Image
from defines import QUES_PATH
from kfile import *
from kimage import *
from kscreen import *
import kchar


def load_questions(dirname):
    queses = []
    for path in os.listdir(dirname):
        name, ext = os.path.splitext(os.path.basename(path))
        if(name[0] != "."):
            queses += load_data(dirname + "/" + path)
    return queses

def show_question(q):
    print(u"type:{0}".format(u"4択" if q["type"] == 0 else u"並び替え"))
    if("genre" in q):
        print(u"genre:{0}".format(q["genre"]))
    if("panel" in q):
        print(u"panel:{0}".format(q["panel"]))
    print(u"question:{0}".format(q["question"]))
    print(u"choices:")
    for c in q["choices"]:
        print(u"\t{0}".format(c))
    print(u"answer:{0}".format(q["answer"]))

# running code ----------------------------------------------

QUESES = load_questions(QUES_PATH)

