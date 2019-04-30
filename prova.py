import ROOT as rt
from ROOT import TLorentzVector
from math import cosh
from itertools import combinations
from operator import itemgetter
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


#histo = rt.TH1F("mjj", "mjj", 200, 124., 124.9)
#histo.SetLineWidth(3)
#histo.GetXaxis().SetTitle("m_{jj} (GeV)")
#histo2 = rt.TH1F("mjj2", "mjj2", 120, 0., 100.)
#histo2.SetLineWidth(3)
#histo2.GetXaxis().SetTitle("m_{jj} (GeV)")



######## MAIN FUNCTION ########
for event in tree:

    print "> event: ", iev
    partons, pids = utils.get_hard_partons(event, 20., debug)
    print "partons PID: ", pids
    
    jets = utils.get_jets(event, 20., debug)
    results, flag = utils.associate_vectors(jets, partons, 10.)
#    print results, flag

    

    mass_pair_b,  other_mass_pair = mjj(partons, pids)
    print "Mass b pairs--->"
    print mass_pair_b
    print "Other pair--->"
    print other_mass_pair

    #see which couple has a mass near to H
    Hpair = utils.nearest_masses_pair(partons, 125.0)
    other_pair = [i for i in range(4) if not i in Hpair]
    print "nearest couple to H mass: ", Hpair    
    print "The other pair: ", other_pair


    if flag ==0:
        # using the results from association we can get
        # the parton-associated jets
        Hjets = [ results[0][iparton]  for iparton in Hpair]
#        other_jets =  [ results[0][iparton]  for iparton in other_pair]
        print "Hjets: ", Hjets
#        print "other_jets", other_jets











#    histo.Fill(mass_pair_b[0][1])
#    histo2.Fill(other_mass_pair[0][1])
      
    
    
    


    print "---------------------------------------------------"
    iev+=1
    if iev>= nevents:
        break


#c1 = rt.TCanvas()
#histo.Draw()
#c1.Print("b_pair.root")

#c2 = rt.TCanvas()
#histo2.Draw()
#c2.Print("other_pair.root")
