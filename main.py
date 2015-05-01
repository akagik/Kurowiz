# -*- encoding: utf-8 -*-
import kdebug

from kivy.config import Config
# initial window size
# they should be changed before importing any modules that affects the application window
Config.set("graphics", "width", 200)
Config.set("graphics", "height",150)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import threading
import kmouse
from time import sleep
from mainloop_reido import MainLoop
from kscreen import captureCurrentWindow

from kscreen import getCurrentImage
from kscreen import change_next_window
from kscreen import change_next_next_window

from recog_ques import get_genre
from recog_ques import get_ques


class LoopRunning(threading.Thread):
    def __init__(self):
        self.stop_event = threading.Event()
        threading.Thread.__init__(self)

    def stop(self):
        self.stop_event.set()
        self.join()

    def run(self):
        loop = MainLoop()

        kmouse.activate()
        change_next_next_window()

        while(not self.stop_event.is_set()):
            change_next_window()
            loop.loop()


class MainWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.loop_button = Button(text="start")
        self.screenshot_button = Button(text="screenshot")
        self.get_ans_button = Button(text="get_answer")

        self.add_widget(self.loop_button)
        self.add_widget(self.screenshot_button)
        self.add_widget(self.get_ans_button)

        self.is_running = False
        self.loop_tread = None

        self.loop_button.bind(on_press=self.toggle_loop)
        self.screenshot_button.bind(on_press=self.do_screenshot)
        self.get_ans_button.bind(on_press=self.get_answer)


    def get_answer(self, *args, **kwargs):
        image = getCurrentImage()
        genre = get_genre(image)

        q, qsim, qcontent = get_ques(image, genre)
        if(q!=None):
            print "answer:", q["answer"]
    
    def do_screenshot(self, *args, **kwargs):
        captureCurrentWindow()

    def toggle_loop(self, *args, **kwargs):
        self.is_running = not self.is_running

        if(self.is_running):
            self.loop_thread = LoopRunning()
            self.loop_thread.setDaemon(True)
            self.loop_thread.start()
            args[0].text = "stop"
        else:
            if(self.loop_thread != None):
                self.loop_thread.stop()
            args[0].text = "start"


class KurowizApp(App):
    def build(self):
        return MainWidget()

KurowizApp().run()
