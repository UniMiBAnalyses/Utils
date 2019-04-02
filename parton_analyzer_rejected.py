import ROOT as rt  
import sys  
import utils
import argparse

parser = argparse.ArgumentParser(description='Parton Analyzer, jet pairing')
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
count_flag2_tot = 0
count_flag2_last = 0
count_flag2_dist = [0.0]*5

for event in tree:

    partons, pids = utils.get_hard_partons(event, debug)
    jets = utils.get_jets(event, debug)

    # Remove top events
    if 6 in pids or -6 in pids:
        continue

    if len(partons) != 4:
        print ">>>> Problem! Event not with only 4 partons!!!! <<<<"

    results, flag = utils.associate_vectors(jets, partons, args.radius)
    if flag == 2:
        count_flag2_tot += 1
        print results
        if results[0][3] == -1:
            # does not have really physical meaning, just a curiosity
            count_flag2_last += 1
        count_flag2_dist[ results[0].count(-1) ] += 1
        unpaired_indices = [i for i, paired in enumerate(results[0]) if paired == -1]
        print unpaired_indices
        for index in unpaired_indices:
            print " pt:   ", partons[index].Pt()
            print " eta: ", partons[index].Eta()

    iev+=1
    if nevents > 0 and iev>= nevents:
        break

print iev, count_flag2_dist, count_flag2_tot, count_flag2_last