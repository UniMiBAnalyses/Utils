import ROOT as rt  
import sys  
import utils
import argparse

parser = argparse.ArgumentParser(description='Count how many t and tbar are present in every event')
parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
parser.add_argument('--nevents', type=int, default=1, help='How many events per file should be analysed. Set to a negative value to include all events')
parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')
parser.add_argument('--radius', type=float, default=0.8, help="Radius from jet")

args = parser.parse_args()

file = rt.TFile(args.data_path)
tree = file.Get("latino")

nevents = args.nevents
debug = args.debug

iev = 0

for event in tree:

    jets = utils.get_jets(event, debug)
    jets_mass = utils.get_jets_changed(event, debug)

    mass_pairs = utils.mjj_pairs(jets)
    print mass_pairs 

    mass_pairs2 = utils.mjj_pairs(jets_mass)
    print mass_pairs2
    
    iev+=1
    if iev>= nevents:
        break