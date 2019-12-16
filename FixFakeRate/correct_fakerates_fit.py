from __future__ import print_function
import ROOT as R 
import argparse
import os
import sys
from itertools import product
from array import array
from math import sqrt

inputfile = R.TFile("output_graph.root", "read")
outputfile = R.TFile("output_fit.root", "recreate")
outputdir = "."
cache = []

fit_results = {}

for i in range(1, 11):  
    g = inputfile.Get("eff_A_L_etabin{}".format(i))
    # f = R.TF1("f_A_L_etabin{}".format(i), "[0] / ( 1 + TMath::Exp((-1)* (x-[1])/ [2]) ) + x*[3] + [4]", 38, 160)
    # f.SetParameter(0, 0.7)
    # f.SetParameter(1, 30)
    # f.SetParameter(2, 10)
    # f.SetParLimits(3, -0.5, 0.5)
    # f.SetParameter(4, 0.1)
    # g.Fit(f,"S", "", 38, 160)
    f = R.TF1("f_A_L_etabin{}".format(i), "[0] + [1]*TMath::Erf((x-[2])/ [3])", 38, 160)
    f.SetParameter(1, 0.7)
    f.SetParameter(2, 30)
    f.SetParameter(3, 10)
    result = g.Fit(f,"S", "", 38, 120)
    result.SetName("fit_result_A_L_etabin{}".format(i))
    #result.Write()

    # c = R.TCanvas()
    # g.Draw("APF")
    # g.SetMarkerStyle(2)
    # c.Draw()
    # cache.append((c,g))
    f.Print()
    g.Write()
    f.Write()
    fit_results["A_L_{}".format(i)] = (f,result)

for i in range(1, 11):  
    g = inputfile.Get("eff_A_T_etabin{}".format(i))
    # f = R.TF1("f_A_T_etabin{}".format(i), "[0] / ( 1 + TMath::Exp((-1)* (x-[1])/ [2]) ) + x*[3] + [4]", 38, 160)
    # f.SetParameter(0, 0.8)
    # f.SetParameter(1, 30)
    # f.SetParameter(2, 10)
    # f.SetParLimits(3, -0.5, 0.5)
    # f.SetParameter(4, 0.1)
    # g.Fit(f,"S", "", 38, 160)
    f = R.TF1("f_A_T_etabin{}".format(i), "[0] + [1]*TMath::Erf((x-[2])/ [3])", 38, 160)
    f.SetParameter(1, 0.8)
    f.SetParameter(2, 30)
    f.SetParameter(3, 10)
    result = g.Fit(f,"S", "", 38, 120)
    result.SetName("fit_result_A_T_etabin{}".format(i))
    #result.Write()

    # c = R.TCanvas()
    # g.Draw("APF")
    # g.SetMarkerStyle(2)
    # c.Draw()
    # cache.append((c,g))

    f.Print()
    g.Write()
    f.Write()
    fit_results["A_T_{}".format(i)] = (f,result)



for i in range(1,11):  
    g = inputfile.Get("eff_B_L_etabin{}".format(i))
    # f = R.TF1("f_B_L_etabin{}".format(i), "[0] / ( 1 + TMath::Exp((-1)* (x-[1])/ [2]) ) + x*[3] + [4]", 30, 160)
    # f.SetParameter(0, 0.9)
    # f.SetParameter(1, 25)
    # f.SetParameter(2, 10)
    # f.SetParLimits(3, -0.5, 0.5)
    # g.Fit(f,"S", "", 30, 160)
    f = R.TF1("f_B_L_etabin{}".format(i), "[0] + [1]*TMath::Erf((x-[2])/ [3])", 30, 160)
    f.SetParameter(1, 0.8)
    f.SetParameter(2, 25)
    f.SetParameter(3, 10)
    result = g.Fit(f,"S", "", 30, 120)
    result.SetName("fit_result_B_L_etabin{}".format(i))
    result.Write()
    # c = R.TCanvas()
    # g.Draw("APF")
    # g.SetMarkerStyle(2)
    # c.Draw()
    # cache.append((c,g))
    f.Print()
    g.Write()
    f.Write()
    fit_results["B_L_{}".format(i)] = (f,result)

for i in range(1,11):  
    g = inputfile.Get("eff_B_T_etabin{}".format(i))
    # f = R.TF1("f_B_T_etabin{}".format(i), "[0] / ( 1 + TMath::Exp((-1)* (x-[1])/ [2]) ) + x*[3] + [4]", 30, 160)
    # f.SetParameter(0, 0.9)
    # f.SetParameter(1, 25)
    # f.SetParameter(2, 10)
    # f.SetParLimits(3, -0.5, 0.5)
    # g.Fit(f,"S", "", 30, 160)
    f = R.TF1("f_B_T_etabin{}".format(i), "[0] + [1]*TMath::Erf((x-[2])/ [3])", 30, 160)
    f.SetParameter(1, 0.9)
    f.SetParameter(2, 25)
    f.SetParameter(3, 10)
    result = g.Fit(f,"S", "", 30, 120)
    result.SetName("fit_result_B_T_etabin{}".format(i))
    result.Write()
    # c = R.TCanvas()
    # g.Draw("APF")
    # g.SetMarkerStyle(2)
    # c.Draw()
    # cache.append((c,g))
    f.Print()
    g.Write()
    f.Write()
    fit_results["B_T_{}".format(i)] = (f,result)


#################################
# Ratio 


pt_bins = array("d",list(range(40,60,2))+ [60,80,100,150,200])
nptbins = len(pt_bins)
print(nptbins, pt_bins)

h2_ratio_tot = R.TH2F("h2_ratio_tot", "", 10, 1, 11, nptbins-1,pt_bins)


mg = R.TMultiGraph()
mgL = R.TMultiGraph()
mgT = R.TMultiGraph()
leg = R.TLegend(0.7,0.56,0.94,0.94)

etabins = [-2.5,-2.1,-1.566,-1.442,-0.8,0.0,0.8,1.442,1.566,2.1,2.5,3]

for etab in range(1,11):
    print(">> eta bin: ", etab)
    g = R.TGraphErrors(nptbins)
    g.SetName("ratio_tot_etabin{}".format(etab))
    g.SetTitle("ratio_tot_etabin{}; Pt (GeV);(A_{{T}}/A_{{L}})/(B_{{T}}/B_{{L}})".format(etab))
    gT = R.TGraphErrors(nptbins)
    gT.SetName("ratio_T_etabin{}".format(etab))
    gT.SetTitle("ratio_T_etabin{}; Pt (GeV);A_{{T}}/B_{{T}}".format(etab))
    gL = R.TGraphErrors(nptbins)
    gL.SetName("ratio_L_etabin{}".format(etab))
    gL.SetTitle("ratio_L_etabin{}; Pt (GeV);B_{{L}}/A_{{L}}".format(etab))

    f_A_T, fit_result_A_T = fit_results["A_T_{}".format(etab)]
    f_A_L, fit_result_A_L = fit_results["A_L_{}".format(etab)]
    f_B_T, fit_result_B_T = fit_results["B_T_{}".format(etab)]
    f_B_L, fit_result_B_L = fit_results["B_L_{}".format(etab)]

    i = 0
    for x in pt_bins:
        eff_A_T = f_A_T.Eval(x)
        eff_A_L = f_A_L.Eval(x)
        eff_B_T = f_B_T.Eval(x)
        eff_B_L = f_B_L.Eval(x)

        xarr = array("d", [x])
        err  = array("d", [0.])

        fit_result_A_T.GetConfidenceIntervals(1,1,1,xarr,err,0.683, False)
        err_A_T = err[0]
        fit_result_A_L.GetConfidenceIntervals(1,1,1,xarr,err,0.683, False)
        err_A_L = err[0]
        fit_result_B_T.GetConfidenceIntervals(1,1,1,xarr,err,0.683, False)
        err_B_T = err[0]
        fit_result_B_L.GetConfidenceIntervals(1,1,1,xarr,err,0.683, False)
        err_B_L = err[0]

        Rtot = (eff_A_T/ eff_A_L) / (eff_B_T / eff_B_L)
        err2_R = err_A_T**2 *( (eff_B_L / eff_B_T) / eff_A_L)**2 + \
                 err_A_L**2 *( (eff_B_L / eff_B_T)*(eff_A_T / eff_A_L**2))**2 +\
                 err_B_T**2 *( (eff_A_T / eff_A_L)*(eff_B_L / eff_B_T**2))**2 +\
                 err_B_L**2 *( (eff_A_T / eff_A_L)*(1/eff_B_T))**2 
        err_R = sqrt(err2_R)
        
        # error propagation
        h2_ratio_tot.SetBinContent(etab,i+1, Rtot)
        g.SetPoint(i, x, Rtot)
        g.SetPointError(i, 0., err_R)
        gL.SetPoint(i, x, eff_B_L / eff_A_L)
        gT.SetPoint(i, x, eff_A_T / eff_B_T)
        i+= 1

    c = R.TCanvas()
    R.gPad.SetLeftMargin(1.3)
    g.Draw("AP")
    g.SetMarkerStyle(8)
    g.SetLineWidth(2)
    gL.SetMarkerStyle(8)
    gL.SetLineWidth(2)
    gT.SetMarkerStyle(8)
    gT.SetLineWidth(2)
    c.Draw()
    cache.append((c,g))
    g.Write()
    c.SaveAs(outputdir+"/"+ g.GetName()+".png")
    if etab not in [3,8]: 
        mg.Add(g)
        mgL.Add(gL)
        mgT.Add(gT)
        leg.AddEntry(g, "eta: {}-{}".format( etabins[etab-1], etabins[etab]))

c = R.TCanvas()
R.gPad.SetLeftMargin(1.3)
mg.Draw("APLX PLC PMC")
mg.SetTitle("R factor by eta;Pt (GeV);R factor")
leg.Draw("same")
c.Draw()
cache.append((c,g))
mg.Write()
c.SaveAs(outputdir+"/all_ratios.png")

c = R.TCanvas()
R.gPad.SetLeftMargin(1.3)
mgL.Draw("APLX PLC PMC")
mgL.SetTitle("B_{L}/A_{L};Pt (GeV);B_{L}/A_{L} factor")
leg.Draw("same")
c.Draw()
cache.append((c,g))
mgL.Write()
c.SaveAs(outputdir+"/loose_ratios.png")

c = R.TCanvas()
R.gPad.SetLeftMargin(1.3)
mgT.Draw("APLX PLC PMC")
mgT.SetTitle("A_{T}/B_{T};Pt (GeV);A_{T}/B_{T} factor")
leg.Draw("same")
c.Draw()
cache.append((c,g))
mgT.Write()
c.SaveAs(outputdir+"/tight_ratios.png")


c = R.TCanvas()
h2_ratio_tot.SetTitle("Ratio tot;Etabin;Pt [GeV]")
h2_ratio_tot.Draw("COLZ")
c.SetLogy()
c.Draw()
c.SaveAs(outputdir+"/"+ h2_ratio_tot.GetName()+".png")
c.Write()



#utputfile.ls()
outputfile.Write()
outputfile.Close()