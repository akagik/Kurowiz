# -*- encoding: utf-8 -*-
import kdebug
from pymouse import PyMouse
from kscreen import *

m = PyMouse()

def get_rel_pos(abs_pos):
    # returns the relative position to window.
    # @param abs_pos the absolute position.
    x = int(abs_pos[0] - window_origin[0]) 
    y = int(-abs_pos[1] + window_origin[1])
    return (x, y)

def get_abs_pos(rel_pos):
    # returns the absolute position.
    # @param rel_pos the position relative to window origin.
    x = int(WINDOW_ORIGIN[0] + rel_pos[0] * ASPECT_RATIO[0])
    y = int(WINDOW_ORIGIN[1] - rel_pos[1] * ASPECT_RATIO[1])
    return (x, y)

def clickAt(pos):
    abspos = get_abs_pos(pos)
    m.click(abspos[0], abspos[1], 1)

def activate():
    m.click(WINDOW_ORIGIN[0] + 5, WINDOW_ORIGIN[1] - 5, 1)

