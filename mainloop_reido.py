# -*- encoding: utf-8 -*-
import kdebug
import random
import time

from klogger import logger
from recog_scene import judge_scene

from kmouse import clickAt
from kmouse import activate

from kscreen import getCurrentImage
from kscreen import SELECT_GENRE_POS
from kscreen import SELECT_ANSWER_POS

from recog_ques import get_genre
from recog_ques import get_choices
from recog_ques import get_ques
from recog_ques import get_answer

from recog_panel import judge_panels

from recog_scene_reido import judge_non_battle_scene, judge_is_non_battle_scene, judge_ans_num
from recog_scene_reido import scene_reido_dictionary
from recog_scene_reido import judge_reido_scene


class MainLoop():
    def __init__(self):
        self.select_panel = None

    def loop(self, default_image=None):
        activate()
        scene_key = judge_reido_scene(default_image)
        
        if(scene_key != None):
            if(scene_key == "is_genre"):
                panels = judge_panels(default_image)
                max_size = -1
                max_num = -1

                click_panel_num = -1
                for i, v in enumerate(panels):
                    # If color is red, select it.
                    if(v[1][0] == 1):
                        click_panel_num = i
                        break
                    if(v[0] > max_size):
                        max_size = v[0]
                        max_num = i
                if(click_panel_num == -1):
                    click_panel_num = max_num
                clickAt(SELECT_GENRE_POS[click_panel_num])
                self.select_panel = panels[click_panel_num]
            elif(scene_key == "is_question"):
                ans_key = judge_ans_num(default_image)
                if(ans_key != None):
                    if(ans_key == "1"):
                        clickAt(SELECT_ANSWER_POS[0])
                    elif(ans_key == "2"):
                        clickAt(SELECT_ANSWER_POS[1])
                    elif(ans_key == "3"):
                        clickAt(SELECT_ANSWER_POS[2])
                    elif(ans_key == "4"):
                        clickAt(SELECT_ANSWER_POS[3])
                else:
                    image = getCurrentImage()
                    genre = get_genre(image)
                    choices = get_choices(image)

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

                    if(qsim < 0.3):
                        clickAt(SELECT_ANSWER_POS[random.randint(0, 3)])
                    else:
                        choice = get_answer(image, q, choices)
                        clickAt(SELECT_ANSWER_POS[choice])
            else:
                pos_box = scene_reido_dictionary[scene_key]["rec_box"]
                clickAt((pos_box[0], pos_box[1]))
                time.sleep(0.3)
                clickAt((pos_box[0]-5, pos_box[1]))
        time.sleep(0.5)

#from PIL import Image
#image = Image.open("temp/questions/1650.png")
#MainLoop().loop(image)
