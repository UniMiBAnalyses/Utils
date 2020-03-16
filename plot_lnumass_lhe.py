import ROOT as R 
import os 
import sys 
import utils
from math import cosh
from itertools import combinations
from operator import itemgetter

file = R.TFile("/afs/cern.ch/work/d/dvalsecc/private/CMSSW_10_2_0/src/LatinoTreesGEN/GenDumper/test/output_lhe.root", "READ")

tree = file.Get("Analyzer/myTree")

h_lnujjmass= R.TH1D("h_lnujjmass", "lnu mass", 100, 0, 200)


for iev, event in enumerate(tree):
    if iev % 1000 == 0: print(".", end="")
    lep = R.TLorentzVector()
    nu = R.TLorentzVector()
    lep.SetPtEtaPhiE(event.lhept1, event.lheeta1, event.lhephi1, event.lhept1*cosh(event.lheeta1))
    nu.SetPtEtaPhiE(event.nu_lhept1, event.nu_lheeta1, event.nu_lhephi1, event.nu_lhept1*cosh(event.nu_lheeta1))

    jets = []
    jetsids = []
    for i in range(1,5):
        jet = R.TLorentzVector()
        # print(getattr(event, f"lhejetpt{i}"), getattr(event, f"lhejeteta{i}"),
        #               getattr(event, f"lhejetphi{i}"),getattr(event, f"lhejetpt{i}"))
        jet.SetPtEtaPhiE(getattr(event, f"lhejetpt{i}"), getattr(event, f"lhejeteta{i}"),
                        getattr(event, f"lhejetphi{i}"),getattr(event, f"lhejetpt{i}")*cosh(getattr(event, f"lhejeteta{i}")))
        jets.append(jet)
        jetsids.append(getattr(event, f"lhejetpdgid{i}"))

    if (lep+nu).M() < 60:
        good_pair = utils.nearest_mass_pair(jets, 80.375)
        W_jets = [j for ij, j in enumerate(jets) if ij in good_pair]
    else: 
        # We are looking at WplusTo2J_WminusToLNu
        W_jets = ()
        Wp = [(2,-1),(2,-3),(2,-5),(4,-1),(4,-3),(4,-5)]
        #print("ids", jetsids)

        masses = []
        for p1,p2 in combinations(range(len(jetsids)),2):
            #print((jetsids[p1],jetsids[p2]))
            if (jetsids[p1],jetsids[p2]) in Wp or (jetsids[p2],jetsids[p1]) in Wp:
                #W_jets = (jets[p1], jets[p2])
                masses.append((jets[p1],jets[p2], (jets[p1]+jets[p2]).M())) 
                #print(jetsids[p1],jetsids[p2],(jets[p1]+jets[p2]).M()) 
        
        #print(list(map(itemgetter(2), masses)))
        # Now get the pair with the smaller mass
        W_jets = sorted(masses, key=itemgetter(2))[0]
        
        
        lnujj = lep + nu + W_jets[0] + W_jets[1]
        #print((good_jets[0] + good_jets[1]).M())
        h_lnujjmass.Fill(lnujj.M())


    
   
c = R.TCanvas()
h_lnujjmass.Draw("hist")
c.SetLogy()
c.Draw()




