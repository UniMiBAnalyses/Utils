import ROOT as rt
from ROOT import TLorentzVector
from math import cosh
from itertools import combinations
from operator import itemgetter
import sys  
import utils

file = rt.TFile(sys.argv[1])
tree = file.Get("latino")


nevents = 100 
if len(sys.argv) > 2:
    nevents = int(sys.argv[2])

debug = False 
if len(sys.argv) > 3:
    debug = bool(sys.argv[3])


iev = 0

def mjj(vectors, pid):
    l = []
    f = []

    for i ,k  in combinations(range(len(pid)),2):
        index = [pid[i],pid[k]]
        if index == [5,-5] or index == [-5,5]:
            
            l.append( [[i,k], (vectors[i]+ vectors[k]).M() ])
        elif pid[i]!=5 and pid[i]!=-5 and pid[k]!=5 and pid[k]!=-5:
            f.append( [[i,k], (vectors[i]+ vectors[k]).M() ])
    l = sorted(l, key=itemgetter(1), reverse=True)
    f = sorted(f, key=itemgetter(1), reverse=True)
    return l, f





######## MAIN FUNCTION ########
for event in tree:

    print "> event: ", iev
    partons, pids = utils.get_hard_partons(event, 10., debug)
    print "partons PID: ", pids
    
    jets = utils.get_jets(event, 10., debug)
    results, flag = utils.associate_vectors(jets, partons, 0.8)
    print "jets association: ", results, flag

    flag2 = 0
    if len(partons) != 4:
        print ">>>> Problem! Event not with 4 partons!!!! <<<<"
        flag2 = -1
        continue


    mass_pair_b,  other_mass_pair = mjj(partons, pids)
    print "Mass b pairs--->", mass_pair_b
    print "Other pair--->", other_mass_pair

       
    if flag ==0:
        # using the results from association we can get
        # the parton-associated jets
        Hjets = [ results[0][iparton]  for iparton in mass_pair_b[0][0]]
        print "Hjets: ", Hjets

        if flag2 != -1:
            other_jets =  [ results[0][iparton]  for iparton in other_mass_pair[0][0]]
            print "other_jets", other_jets

    else:
        print ">>>> Jets association gone wrong <<<<"




   


    print "---------------------------------------------------"
    iev+=1
    if iev>= nevents:
        break


