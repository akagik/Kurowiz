# -*- encoding: utf-8 -*-
import kdebug
import time
import random

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

from recog_panel import judge_panels

class MainLoop():
    def __init__(self):
        self.select_panel = None

    def loop(self, default_image=None):
        scene_key = judge_scene(default_image)

        # select genre
        if(scene_key == "is_genre"):
            logger.debug("genre select")
            panels = judge_panels(default_image)

            # 色が青・赤、または色が一番多いパネルを選択
            max_size = -1
            max_num = -1
            for i, v in enumerate(panels):
                # If color is red, select it.
                if(v[1][0] == 1 or v[1][0] == 0):
                    click_panel_num = i
                    break
                if(v[0] > max_size):
                    max_size = v[0]
                    max_num = i
            if(click_panel_num == -1):
                click_panel_num = max_num

            clickAt(SELECT_GENRE_POS[click_panel_num])
            self.select_panel = panels[click_panel_num]

        # select question answer
        elif(scene_key == "is_question"):
            logger.debug("question select")

            image = getCurrentImage()
            genre = get_genre(image)
            choices = get_choices(image)
            time.sleep(2.2)

            image = getCurrentImage()

            panel = None
            if(self.select_panel != None):
                if(self.select_panel[0] == 1):
                    panel = u"1色"
                if(self.select_panel[0] == 2):
                    panel = u"2色"
                if(self.select_panel[0] == 3):
                    panel = u"3色"
                else:
                    panel = None 
            q, qsim, qcontent = get_ques(image, genre, panel)
            
            if(q!=None):
                logger.debug(q["question"])

            print "qsim:", qsim
            if(qsim < 0.3):
                clickAt(SELECT_ANSWER_POS[random.randint(0, 3)])
                time.sleep(1)
                ansnum = judge_ansnum()
                if(ansnum != -1):
                    print "answer nubmer:", ansnum
                else:
                    print "answer number:", "読み取り不能"

            else:
                print "answer:", q["answer"]
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
        time.sleep(0.5)

#from PIL import Image
#image = Image.open("temp/genre/genre3.png")
#MainLoop().loop(image)
