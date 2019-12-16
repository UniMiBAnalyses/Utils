from __future__ import print_function
import ROOT as R 
import argparse
import os
import sys
from itertools import product


A_loose = R.TFile("2017_trigger_eff/Ele35_pt_eta_EGM_2017Bv6_onlyLoosenominal_efficiency.root")
A_tight = R.TFile("2017_trigger_eff/Ele35_pt_eta_EGM_2017Bv6_nominal_efficiency.root")
B_loose = R.TFile("2017_trigger_eff/Ele23_Ele12_leg1_pt_eta_EGM_2017Bv6_onlyLoosenominal_efficiency.root")
B_tight = R.TFile("2017_trigger_eff/Ele23_Ele12_leg1_pt_eta_EGM_2017Bv6_nominal_efficiency.root")

print ("Aloose",[p for p in A_loose.c.GetListOfPrimitives()])
print ("Atight",[p for p in A_tight.c.GetListOfPrimitives()])
print ("Bloose",[p for p in B_loose.c.GetListOfPrimitives()])
print ("Btight",[p for p in B_tight.c.GetListOfPrimitives()])

eff_A_L = A_loose.c.GetPrimitive("Ele35_pt_eta_total_clone")
eff_A_T = A_tight.c.GetPrimitive("Ele35_pt_eta_total_clone")
eff_B_L = B_loose.c.GetPrimitive("Ele23_Ele12_leg1_pt_eta_total_clone")
eff_B_T = B_tight.c.GetPrimitive("Ele23_Ele12_leg1_pt_eta_total_clone")

hs = [eff_A_L, eff_A_T, eff_B_L, eff_B_T]
cache =[]
for i,h in enumerate(hs):
    c = R.TCanvas(h.GetTitle()+str(i))
    h.Draw("COLZ")
    c.Draw()
    cache.append(c)

# Get histogram to copy the structure
h_A_L = eff_A_L.GetCopyTotalHisto()
h_A_T = eff_A_T.GetCopyTotalHisto()
h_B_L = eff_B_L.GetCopyTotalHisto()
h_B_T = eff_B_T.GetCopyTotalHisto()

binsX_A = h_A_L.GetNbinsX()
binsX_B = h_B_L.GetNbinsX()
binsY_A = h_A_L.GetNbinsY()
binsY_B = h_B_L.GetNbinsY()


outputfile = R.TFile("output_graph.root", "recreate")

bypt = {}

for binx in range(1, binsX_A+1):
    print("bin edge", binx,  h_A_L.GetXaxis().GetBinLowEdge(binx), h_A_L.GetXaxis().GetBinUpEdge(binx))

    g = R.TGraphAsymmErrors(binsY_A)
    i = 0
    for biny in range(1, binsY_A+1):
        gbin = eff_A_L.GetGlobalBin(binx,biny)
        #print(i, h_A_L.GetYaxis().GetBinCenter(biny), eff_A_L.GetEfficiency(gbin))
        g.SetPoint(i, h_A_L.GetYaxis().GetBinCenter(biny), eff_A_L.GetEfficiency(gbin))
        g.SetPointError(i, 0., 0., eff_A_L.GetEfficiencyErrorLow(gbin), eff_A_L.GetEfficiencyErrorUp(gbin))
        i+=1
    bypt[binx] = g
    g.SetName("eff_A_L_etabin{}".format(binx))
    g.SetTitle("eff_A_L_etabin{};Pt".format(binx))
    g.Write()

for binx in range(1, binsX_A+1):
    g = R.TGraphAsymmErrors(binsY_A)
    i = 0
    for biny in range(1, binsY_A+1):
        gbin = eff_A_T.GetGlobalBin(binx,biny)
        #print(i, h_A_T.GetYaxis().GetBinCenter(biny), eff_A_T.GetEfficiency(gbin))
        g.SetPoint(i, h_A_T.GetYaxis().GetBinCenter(biny), eff_A_T.GetEfficiency(gbin))
        g.SetPointError(i, 0., 0., eff_A_T.GetEfficiencyErrorLow(gbin), eff_A_T.GetEfficiencyErrorUp(gbin))
        i+=1
    bypt[binx] = g
    g.SetName("eff_A_T_etabin{}".format(binx))
    g.SetTitle("eff_A_T_etabin{};Pt".format(binx) )
    g.Write()
    
for binx in range(1, binsX_B+1):
    g = R.TGraphAsymmErrors(binsY_B)
    i = 0
    for biny in range(1, binsY_B+1):
        gbin = eff_B_L.GetGlobalBin(binx,biny)
        #print(i, h_B_L.GetYaxis().GetBinCenter(biny), eff_B_L.GetEfficiency(gbin))
        g.SetPoint(i, h_B_L.GetYaxis().GetBinCenter(biny), eff_B_L.GetEfficiency(gbin))
        g.SetPointError(i, 0., 0., eff_B_L.GetEfficiencyErrorLow(gbin), eff_B_L.GetEfficiencyErrorUp(gbin))
        i+=1
    bypt[binx] = g
    g.SetName("eff_B_L_etabin{}".format(binx))
    g.SetTitle("eff_B_L_etabin{};Pt".format(binx) )
    g.Write()

for binx in range(1, binsX_B+1):
    g = R.TGraphAsymmErrors(binsY_B)
    i = 0
    for biny in range(1, binsY_B+1):
        gbin = eff_B_T.GetGlobalBin(binx,biny)
        #print(i, h_B_T.GetYaxis().GetBinCenter(biny), eff_B_T.GetEfficiency(gbin))
        g.SetPoint(i, h_B_T.GetYaxis().GetBinCenter(biny), eff_B_T.GetEfficiency(gbin))
        g.SetPointError(i, 0., 0., eff_B_T.GetEfficiencyErrorLow(gbin), eff_B_T.GetEfficiencyErrorUp(gbin))
        i+=1
    bypt[binx] = g
    g.SetName("eff_B_T_etabin{}".format(binx))
    g.SetTitle("eff_B_T_etabin{};Pt".format(binx) )
    g.Write()


outputfile.Write()
# outputfile.Close()