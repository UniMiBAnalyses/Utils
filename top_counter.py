import ROOT as rt  
import sys  
import utils
import os
import argparse

parser = argparse.ArgumentParser(description='Count how many t and tbar are present in every event')
parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
parser.add_argument('--nevents', type=int, default=-1, help='How many events per file should be analysed. Set to a negative value to include all events')
parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')

args = parser.parse_args()

# data_path = '/gwteray/users/govoni/OneLeptonSkims/VBS_semileptonic_signal_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l1tightChain__LepTrgFix__dorochester__formulasMC/'
data_path = args.data_path
nevents = args.nevents
debug = args.debug
file_list = os.listdir(data_path)

print 'file iev no_t_no_tbar t tbar t_tbar'

for f in sorted(file_list):
    file = rt.TFile(data_path + '/' + f)
    tree = file.Get("latino")

    iev = 0
    count_tbar = 0
    count_t = 0
    count_no_t_tbar = 0
    for event in tree:

        # print "> event: ", iev
        partons, pids = utils.get_hard_partons(event, debug)

        # print "partons PID: ", pids
        index_t = -1
        index_tbar = -1
        found_t = False
        found_tbar = False
        try:
            index_t = pids.index(6) 
            found_t = True
        except:
            pass
        try:
            index_tbar = pids.index(-6)
            found_tbar = True
        except:
            pass
        if found_t:
            count_t += 1
        if found_tbar:
            count_tbar +=1
        if (not found_t) and (not found_tbar):
            count_no_t_tbar += 1
        # print index_t, index_tbar

        mass_pairs = utils.mjj_pairs(partons)
        eta_pairs = utils.deltaeta_pairs(partons)
        # print "Mass pairs"
        # print mass_pairs
        # print "Eta pairs"
        # print eta_pairs

        iev+=1
        if nevents > 0 and iev >= nevents:
            break
    print f, iev, count_no_t_tbar, count_t, count_tbar, count_t + count_tbar + count_no_t_tbar - iev