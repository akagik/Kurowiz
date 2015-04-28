# -*- encoding: utf-8 -*-
import kdebug
import time

from klogger import logger
from recog_scene import judge_scene
from recog_scene import judge_ansnum
from recog_scene import judge_erratum

from kmouse import clickAt

from kscreen import getCurrentImage
from kscreen import SELECT_GENRE_POS
from kscreen import SELECT_ANSWER_POS

from recog_ques import get_genre
from recog_ques import get_choices
from recog_ques import get_ques
from recog_ques import get_answer
import random

def mainloop():
    scene_key = judge_scene()
    if(scene_key == "is_genre"):
        print("genre select")
        clickAt(SELECT_GENRE_POS[random.randint(0,3)])
    elif(scene_key == "is_question"):
        print("question select")
        image = getCurrentImage()
        genre = get_genre(image)
        choices = get_choices(image)
        time.sleep(2.3)
        image = getCurrentImage()
        q, qsim, qcontent = get_ques(image, genre)
        
        print q["question"]
        print "qsim:", qsim
        if(qsim < 0.3):
            clickAt(SELECT_ANSWER_POS[random.randint(0, 3)])
            time.sleep(1)
            ansnum = judge_ansnum()
            if(ansnum != -1):
                print "answer nubmer:", ansnum
            else:
                print "answer number:", "読み取り不能"
            save_q = {}
            save_q["genre"] = genre
            save_q["question"] = qcontent
            save_q["answer"] = choices[ansnum-1]

#            QUESTIONS.append(save_q)
#            kfile.dump_data([save_q], "questions/question_{0}.dat".format(qcontent.encode("utf-8")))
        else:
            choice = get_answer(image, q, choices)
            if(choice == -1):
                logger.debug("Unknown question...")
            else:
                logger.debug("Known question!!!")

            clickAt(SELECT_ANSWER_POS[choice])
            time.sleep(1)

            erratum_key = judge_erratum()
            if(erratum_key == "is_seikai"):
                print("正解!")
            elif(erratum_key == "is_hazure"):
                print("不正解...")
            else:
                print("判別不能")
    time.sleep(2)

