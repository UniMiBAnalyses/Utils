import utils 
import ROOT as rt  
import sys  
from itertools import combinations
from operator import itemgetter

file = rt.TFile(sys.argv[1])
tree = file.Get("latino")

nevents = 10
if len(sys.argv) > 2:
    nevents = int(sys.argv[2])


def mjj_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], (vectors[i]+ vectors[k]).M() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l

def deltaeta_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta()- vectors[k].Eta()) ) )
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l

def deltaR_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], vectors[i].DeltaR(vectors[k])) )
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l


iev = 0

for event in tree:
    print "> event: ", iev
    ids = [int(pid) for pid in event.std_vector_partonGen_pid if pid!=-9999]
    print "partons PID: ",ids
    partons = utils.get_quadrimomenta(event.std_vector_partonGen_pt, 
                                      event.std_vector_partonGen_eta, 
                                      event.std_vector_partonGen_phi, debug=True)
    
    #masse invarianti
    masses = mjj_pairs(partons)
    print masses

    iev+=1
    if iev> nevents:
        break