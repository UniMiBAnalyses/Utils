from __future__ import print_function
import ROOT as R 
import argparse
import os
import sys
from itertools import product
from array import array

inputfile = R.TFile(sys.argv[1], "read")
outputfile = R.TFile(sys.argv[2], "recreate")
#outputdir = "/eos/user/d/dvalsecc/www/VBSPlots/2017_checks/fake_rate_correction/"
outputdir = "."
cache = []

pt_bins = array("d",list(range(40,60,2))+ [60,100,150,200])
nptbins = len(pt_bins)
print(nptbins, pt_bins)

h2_ratio_tot = R.TH2F("h2_ratio_tot", "", 10, 1, 11, nptbins-1,pt_bins)



for etab in range(1,11):
    print(">> eta bin: ", etab)
    g = R.TGraph(nptbins)
    g.SetName("ratio_tot_etabin{}".format(etab))
    g.SetTitle("ratio_tot_etabin{}; Pt (GeV);(A_{{T}}/A_{{L}})/(B_{{T}}/B_{{L}})".format(etab))
    f_A_T = inputfile.Get("f_A_T_etabin{}".format(etab))
    f_A_L = inputfile.Get("f_A_L_etabin{}".format(etab))
    f_B_T = inputfile.Get("f_B_T_etabin{}".format(etab))
    f_B_L = inputfile.Get("f_B_L_etabin{}".format(etab))
    fit_result_A_T = inputfile.Get("fit_result_A_T_etabin{}".format(etab))
    fit_result_A_L = inputfile.Get("fit_result_A_L_etabin{}".format(etab))
    fit_result_B_T = inputfile.Get("fit_result_B_T_etabin{}".format(etab))
    fit_result_B_L = inputfile.Get("fit_result_B_L_etabin{}".format(etab))


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
        print(err_A_T, err_A_L)


        ratio_tot = (eff_A_T/ eff_A_L) / (eff_B_T / eff_B_L)
        h2_ratio_tot.SetBinContent(etab,i+1, ratio_tot)
        g.SetPoint(i, x, ratio_tot)
        i+= 1

    c = R.TCanvas()
    R.gPad.SetLeftMargin(1.3)
    g.Draw("APL")
    c.Draw()
    cache.append((c,g))
    g.Write()
    c.SaveAs(outputdir+"/"+ g.GetName()+".png")

c = R.TCanvas()
h2_ratio_tot.SetTitle("Ratio tot;Etabin;Pt [GeV]")
h2_ratio_tot.Draw("COLZ")
c.SetLogy()
c.Draw()
c.SaveAs(outputdir+"/"+ h2_ratio_tot.GetName()+".png")
c.Write()

# outputfile.Write()
# outputfile.Close()

