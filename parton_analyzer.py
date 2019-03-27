import ROOT as rt  
import sys  
import utils

file = rt.TFile(sys.argv[1])
tree = file.Get("latino")

nevents = 10
if len(sys.argv) > 2:
    nevents = int(sys.argv[2])

debug = False 
if len(sys.argv) > 3:
    debug = bool(sys.argv[3])


iev = 0

for event in tree:
    print "> event: ", iev
    partons, pids = utils.get_hard_partons(event, debug)

    print "partons PID: ", pids
    print "partons: ", partons
    
    mass_pairs = utils.mjj_pairs(partons)
    eta_pairs = utils.deltaeta_pairs(partons)
    print "Mass pairs"
    print mass_pairs
    print "Eta pairs"
    print eta_pairs

    iev+=1
    if iev>= nevents:
        break