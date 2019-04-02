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

    partons, pids = utils.get_hard_partons(event, debug)
    jets = utils.get_jets(event, debug)

    # Remove top events
    if 6 in pids or -6 in pids:
        continue

    print "> event: ", iev
    iev+=1
    print "partons PID: ", pids
    print "partons: ", partons

    results, flag = utils.associate_vectors(jets, partons, args.radius)
    print results, flag

    # get the pair nearest  to W or Z mass
    vpair = utils.nearest_masses_pair(partons, [80.385, 91.1876])
    print(vpair)
    v_partons = [partons.pop(vpair[0]), partons.pop(vpair[1]-1)]
    
    if flag == 0:
        pass

    
    if iev>= nevents:
        break