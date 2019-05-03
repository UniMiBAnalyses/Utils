import ROOT as rt
from ROOT import TLorentzVector
from math import cosh, sqrt
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


def get_bjets(event, ptmin, debug):
    bjets = []
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

    notb_jets = jets
    l = [b_jet1, b_jet2]
    l.sort()
   

    return jets, notb_jets, l 

def min_deltaeta_pairs(vectors, hpair):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta()- vectors[k].Eta()) ) )
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]


def max_pt_pair(vectors):
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

def nearest_mass_pair(vectors, mass):
    ''' Returns the pair of vectors with invariant mass nearest to 
    the given mass '''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], abs(mass - (vectors[i]+ vectors[k]).M() )))  
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]


######## MAIN FUNCTION ########
for event in tree:

    print "> event: ", iev
#    partons, pids = utils.get_hard_partons(event, 10., debug)
#    print "partons PID: ", pids
    
#    jets = utils.get_jets(event, 10., debug)
#    results, flag = utils.associate_vectors(jets, partons, 0.8)
#    print "jets association: ", results, flag

  
    
    
    jets, nonbjets, hpair = get_bjets(event,  20., debug)
    print "number of jets: ", len(jets)
    print "number of others: ", len(nonbjets)
    print "Hpair: ", hpair     


    wjets = nearest_mass_pair(jets, 80.385)
    print "W jets con nearest mass: ", wjets

    wjets = max_pt_pair(jets)
    print "W jets con pt max: ", wjets

    wjets = min_deltaeta_pairs(jets, hpair)
    print "W jets con delta eta min: ", wjets


#    flag2 = 0
#    if len(partons) != 4:
#        print ">>>> Problem! Event not with 4 partons!!!! <<<<"
#        flag2 = -1
#        continue
#

#    mass_pair_b,  other_mass_pair = mjj(partons, pids)
#    print "Mass b pairs--->", mass_pair_b
#    print "Other pair--->", other_mass_pair
#
       
#    if flag ==0:
#        # using the results from association we can get
#        # the parton-associated jets
#        Hjets = [ results[0][iparton]  for iparton in mass_pair_b[0][0]]
#        print "Hjets: ", Hjets
#
##        prova = utils.nearest_masses_pair(jets, 125.0)
##        print "PROVA: ", prova
#


#        if flag2 != -1:
#            other_jets =  [ results[0][iparton]  for iparton in other_mass_pair[0][0]]
#            print "other_jets", other_jets
#
#    else:
#        print ">>>> Jets association gone wrong <<<<"
#



   


    print "---------------------------------------------------"
    iev+=1
    if iev>= nevents:
        break


