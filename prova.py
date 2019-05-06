import ROOT as rt
from ROOT import TLorentzVector
from math import cosh, sqrt
from itertools import combinations
from operator import itemgetter
import sys  
import utils
import numpy

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


def get_bjets(event, ptmin, debug):
    jets = []
    l = []
    
    maxbtag1 = max(event.std_vector_jet_DeepCSVB)
    maxbtag2 = -9999.
    b_jet1 = 0
    b_jet2 = 0
    
         
 

    index = 0
   
    for pt, eta, phi,mass, bvalue in  zip(event.std_vector_jet_pt, 
                     event.std_vector_jet_eta, event.std_vector_jet_phi, 
                     event.std_vector_jet_mass, event.std_vector_jet_DeepCSVB):
         
        
        if pt < 0 or pt < ptmin:
            break
        if abs(eta) < 10 :
            p = pt * cosh(eta)
            vec = TLorentzVector()
            en = sqrt(p**2 + mass**2)

            vec.SetPtEtaPhiE(pt, eta, phi, en)
            
            if bvalue == maxbtag1:
                b_jet1 = index
            elif bvalue > maxbtag2:
                maxbtag2 = bvalue
                b_jet2 = index                     

            jets.append(vec)
    
        index+=1


    l = [b_jet1, b_jet2]
    l.sort()
   

    return jets,  l 

def min_deltaeta_pairs(vectors, hpair):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta()- vectors[k].Eta()) ) )
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]


def max_pt_pair(vectors, hpair):
    ''' Returns the pair with highest Pt'''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(( [i,k], (vectors[i]+ vectors[k]).Pt() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]

def nearest_mass_pair(vectors, mass, hpair):
    ''' Returns the pair of vectors with invariant mass nearest to 
    the given mass '''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], abs(mass - (vectors[i]+ vectors[k]).M() )))  
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1] and \
           l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]:
            return  l[i][0]

def get_jets_and_bscore(event, ptmin=20., debug=False):
    jets = []
    b_scores = []

    for pt, eta, phi,mass, bvalue in  zip(event.std_vector_jet_pt, 
                     event.std_vector_jet_eta, event.std_vector_jet_phi, 
                     event.std_vector_jet_mass, event.std_vector_jet_DeepCSVB):

        if pt < 0 or pt < ptmin:
            break
        if abs(eta) < 10 :
            p = pt * cosh(eta)
            vec = TLorentzVector()
            en = sqrt(p**2 + mass**2)
            vec.SetPtEtaPhiE(pt, eta, phi, en)
            jets.append(vec)
            b_scores.append(bvalue)
    
    return jets, b_scores

######## MAIN FUNCTION ########
for event in tree:

    print "> event: ", iev
#    partons, pids = utils.get_hard_partons(event, 10., debug)
#    print "partons PID: ", pids
    
#    jets = utils.get_jets(event, 10., debug)
#    results, flag = utils.associate_vectors(jets, partons, 0.8)
#    print "jets association: ", results, flag

    hpair = [-1,-1]
    wpair = [-1,-1]
    H_jets = numpy.zeros(2, dtype=numpy.int32)
    W_jets = numpy.zeros(2, dtype=numpy.int32)
    
#    jets, hpair = get_bjets(event,  20., debug)
#    print "number of jets: ", len(jets)
#    print "number of others: ", len(nonbjets)
#    print "Hpair: ", hpair     


#    wjets = nearest_mass_pair(jets, 80.385, hpair)
#    print "W jets con nearest mass: ", wjets
#
#    wjets = max_pt_pair(jets)
#    print "W jets con pt max: ", wjets
#
#    wjets = min_deltaeta_pairs(jets, hpair)
#    print "W jets con delta eta min: ", wjets
#
  
#    H_jets[0], H_jets[1] = hpair 
#    W_jets[0], W_jets[1] = wpair 
#    print "H_jets: ", H_jets
#    print "W_jets: ", W_jets

    print "---secondo metodo---"

    jets, b_scores = get_jets_and_bscore(event, 20., debug)
    bjets = [(i, bscore) for i, bscore in enumerate(b_scores)
               if bscore >= 0.63]
    print "bscores: ", b_scores
    print "bjets 1: ", bjets


    if len(bjets) >= 2:
    # Take the indexes of the two jets with bigger bscore
        hpair = [j[0] for j in list(sorted(bjets, key=itemgetter(1), reverse=True))[:2]]

        print "hpair: ", hpair

        if len(jets) >=4:
            wpair = nearest_mass_pair(jets, 80.385, hpair)

        print "wpair: ", wpair

    H_jets[0], H_jets[1] = hpair
    W_jets[0], W_jets[1] = wpair

    print "H_jets: ", H_jets
    print "W_jets: ", W_jets

#    if len(partons) >= 2:
#        bpair = [i for i, p in enumerate(pids) if p in [5,-5]]
#
#    print "i b sono: ", bpair
#
#
#    if len(partons) >= 4 and len(bpair) == 2:
#         wpair = nearest_mass_pair(partons, 80.385, bpair)
##        wpair = max_pt_pair(partons, bpair)
##        wpair = min_deltaeta_pairs(partons, bpair)
#    print "wpair: ", wpair



       
#    if flag ==0:
#        # using the results from association we can get
#        # the parton-associated jets
#        for ip, iparton in enumerate(bpair):
#            H_jets[ip] = results[0][iparton]
#        for jp, jparton in enumerate(wpair):
#            W_jets[jp] = results[0][jparton] 



#        if flag2 != -1:
#            other_jets =  [ results[0][iparton]  for iparton in other_mass_pair[0][0]]
#            print "other_jets", other_jets
#
#    else:
#        print ">>>> Jets association gone wrong <<<<"




   


    print "---------------------------------------------------"
    iev+=1
    if iev>= nevents:
        break


