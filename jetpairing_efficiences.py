import ROOT as rt  
import sys  
import utils
import os
import argparse
import multiprocessing
from functools import partial
from contextlib import contextmanager
import numpy
from ROOT import TLorentzVector
from math import cosh, sqrt
from itertools import combinations
from operator import itemgetter
import argparse

parser = argparse.ArgumentParser(description='Count how many t and tbar are present in every event')
parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
parser.add_argument('--nevents', type=int, default=1, help='How many events per file should be analysed. Set to a negative value to include all events')

args = parser.parse_args()

file = rt.TFile(args.data_path)
tree = file.Get("latino")

nevents = 

iev = 0
counter_ev = 0
match = 0
for event in tree:
    

    if event.H_jets_true == event.H_jets:
        counter_ev += 1
        if event.W_jets_true == event.W_jets:
            match +=1
        



    iev+=1
    if iev>= nevents:
        break

efficiency = match/counter_ev
print "efficiency: ", efficiency

