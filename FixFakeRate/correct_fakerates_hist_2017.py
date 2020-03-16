from __future__ import print_function
import ROOT as R 
import argparse
import os
import sys
from itertools import product


A_loose = R.TFile("ArunTriggerEff/Ele35_pt_eta_EGM_2017Bv6_onlyLoosenominal_efficiency.root")
A_tight = R.TFile("ArunTriggerEff/Ele35_pt_eta_EGM_2017Bv6_nominal_efficiency.root")
B_loose = R.TFile("ArunTriggerEff/Ele23_Ele12_leg1_pt_eta_EGM_2017Bv6_onlyLoosenominal_efficiency.root")
B_tight = R.TFile("ArunTriggerEff/Ele23_Ele12_leg1_pt_eta_EGM_2017Bv6_nominal_efficiency.root")

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


binsX = h_A_L.GetNbinsX()

if h_A_T.GetNbinsX() != binsX: print("ERROR X A_T")
if h_B_L.GetNbinsX() != binsX: print("ERROR X B_L")
if h_B_T.GetNbinsX() != binsX: print("ERROR X B_T")
edX_A = [h_A_L.GetXaxis().GetBinLowEdge(i) for i in range(1, binsX+1)]
edX_B = [h_B_L.GetXaxis().GetBinLowEdge(i) for i in range(1, binsX+1)]
print("edge X A: ", edX_A)
print("edge X B: ", edX_B)

binsY = h_A_L.GetNbinsY()
binsY_B = h_B_L.GetNbinsY()
if h_A_T.GetNbinsY() != binsY: print("ERROR Y A_T")
if h_B_L.GetNbinsY() != binsY: print("ERROR Y B_L")
if h_B_T.GetNbinsY() != binsY: print("ERROR Y B_T")
edY_A = [h_A_L.GetYaxis().GetBinLowEdge(i) for i in range(1, binsY+1)]
edY_B = [h_B_L.GetYaxis().GetBinLowEdge(i) for i in range(1, binsY+1)]
edY_A_up = [h_A_L.GetYaxis().GetBinUpEdge(i) for i in range(1, binsY+1)]
edY_B_up = [h_B_L.GetYaxis().GetBinUpEdge(i) for i in range(1, binsY+1)]
print("edge X A: ", edY_A)
print("edge up X A: ", edY_A_up)
print("edge X B: ", edY_B)
print("edge up X B: ", edY_B_up)
print("N bins A:", binsY, "N bins B: ", binsY_B)


outputfile = R.TFile("output.root", "recreate")
ratio_L = h_A_L.Clone("ratio_L")
ratio_T = h_B_T.Clone("ratio_T")
ratio_L.SetTitle("Eff. Loose trig A/B")
ratio_T.SetTitle("Eff. Tight trig A/B")
ratio_tot = ratio_L.Clone("ratio_tot")
ratio_tot.SetTitle("ratio_tot")
ratio_L.Reset()
ratio_T.Reset()
ratio_tot.Reset()

ratios_pt = {}

for binx in range(1, binsX+1):
    g = R.TGraph(binsY - 2)
    g.SetName("ratio_etabin{}".format(binx))
    g.SetTitle("ratio_etabin{};Pt".format(binx) )
    g.Write()
    ratios_pt[binx] = g

# No overflow and underflow for eta, 
# Starting from bin3, 40 GeV in Pt
for binx, biny in product(range(1, binsX+1), range(3, binsY+2)):
    eAL = eff_A_L.GetEfficiency(eff_A_L.GetGlobalBin(binx, biny))
    eBL = eff_B_L.GetEfficiency(eff_B_L.GetGlobalBin(binx, biny))
    eAT = eff_A_T.GetEfficiency(eff_A_T.GetGlobalBin(binx, biny))
    eBT = eff_B_T.GetEfficiency(eff_B_T.GetGlobalBin(binx, biny))

    if eBL == 0 or eBT == 0:
        print(binx, biny,eff_A_L.GetGlobalBin(binx, biny), eAL, eAT, eBL, eBT)
        ratio_L.SetBinContent(binx, biny, 1)
        ratio_T.SetBinContent(binx, biny, 1)
        ratio_tot.SetBinContent(binx, biny, 1)
        ratios_pt[binx].SetPoint(biny-3, h_A_L.GetYaxis().GetBinCenter(biny), eAL)
    else:
        ratio_L.SetBinContent(binx, biny, eAL / eBL)
        ratio_T.SetBinContent(binx, biny, eAT / eBT)
        ratio_tot.SetBinContent(binx, biny, (eAT / eAL) / (eBT / eBL))
        print(h_A_L.GetYaxis().GetBinCenter(biny))
        ratios_pt[binx].SetPoint(biny-3, h_A_L.GetYaxis().GetBinCenter(biny), eAL)

cL = R.TCanvas("cl")
ratio_L.Draw("COLZ")
cL.SetLogy()
cL.Draw()

cT = R.TCanvas("cT")
ratio_T.Draw("COLZ")
cT.SetLogy()
cT.Draw()

cTot = R.TCanvas("cTot")
ratio_tot.Draw("COLZ")
cTot.SetLogy()
cTot.Draw()


outputfile.Write()
# outputfile.Close()