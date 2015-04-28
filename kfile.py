# -*- encoding: utf-8 -*-
import kdebug
import pickle
import os

def load_data(filename):
    data = 0
    if(os.path.exists(filename)):
        f = open(filename, "r")
        data = pickle.load(f)
        f.close()
    else:
        print "Error: file not exists :", filename
    return data

def dump_data(data, filename):
    f = open(filename, "w")
    pickle.dump(data, f)
    f.close()

