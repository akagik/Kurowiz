#!/home/kohei/.pyenv/shims/python
# -*- encoding: utf-8 -*-
import sys
sys.path.append('..')

import kdebug
import kchar
from kimage import *
from kfont import get_word_image
from PIL import Image
from kfile import dump_data


ch_dir = kchar.CH_DIR
keys = sorted(ch_dir)

ch_sim_dir = {}

for i, keyi in enumerate(keys):
    for j, keyj in enumerate(keys[i:]):
        sim = calc_sim_b(ch_dir[keyi], ch_dir[keyj])
        print keyi, "-", keyj, ":", sim
        ch_sim_dir[frozenset([keyi, keyj])] = sim
dump_data(ch_sim_dir, "ch_sim_dir.dat")
