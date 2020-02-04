'''
Ratio normalized( Data ) / normalized( MC )


'''

import ROOT as R
import sys
import argparse
from math import sqrt


parser = argparse.ArgumentParser()
parser.add_argument("--inputfile", type=str, help="mkShape rootFile")
parser.add_argument("--output", type=str, help="Path to file containing the correction function")
parser.add_argument("--var",type=str, help="Variable whose disrtibution is used to compute the new set of weights")
parser.add_argument("--samples",nargs="+", type=str, help="Samples (space-separated list)")
parser.add_argument("--sample-to-reweight",type=str, help="Sample to be reweighted")
parser.add_argument("--cat", type=str, help="Category (only a single category is considered!)")
parser.add_argument("--fit-func", type=str, help="Fit function expression")
parser.add_argument("--fit-range", nargs=2, type=float, help="Fit range")
args = parser.parse_args()

samples = args.samples
cat = args.cat

log = open("{}_{}_{}_log.txt".format(args.sample_to_reweight, args.cat, args.var), "w")
log.write("Samples: Data,{}\n".format(",".join(args.samples)))
log.write("Sample to reweight: {}\n".format(args.sample_to_reweight))
log.write("Cat: {}\n".format(args.cat))
log.write("Var: {}\n".format(args.var))
log.write("Fit func: {}\n".format(args.fit_func))
log.write("Fit range: {}\n".format(args.fit_range))

#########################################
# Read the histograms

f = R.TFile(args.inputfile)
hs = {}
tot_mc = None

for s in samples:
    h = f.Get(cat+ "/"+args.var+"/histo_"+s)
    print (h)
    hs[s] = h
    if tot_mc:
        tot_mc.Add(h)
    else:
        tot_mc = h.Clone()
        tot_mc.SetName("totMC") 

data_hist = f.Get(cat+ "/"+args.var+"/histo_DATA")
# Remove all others MC from data
data_hist.Add(tot_mc, -1)

reweight_hist = f.Get(cat + "/"+ args.var +"/histo_"+args.sample_to_reweight)


# Ratio: normalized distribution!
reweight_hist.Scale(1/ reweight_hist.Integral())
data_hist.Scale(1/data_hist.Integral())

c1 = R.TCanvas()
leg1 = R.TLegend()
reweight_hist.Draw("hist")
reweight_hist.SetLineColor(R.kRed)
data_hist.Draw("hist same")
leg1.AddEntry(reweight_hist, args.sample_to_reweight+" normed", "l")
leg1.AddEntry(data_hist, "data-MCs normed", "l")
leg1.Draw()
c1.Draw()

nbins = data_hist.GetNbinsX()

weights = []
xbin = []
xcenter = []
errw = []

g = R.TGraphErrors()
g.SetTitle("data-MC ratio")
g.SetMarkerStyle(7)
g.SetMarkerSize(3)
g.GetXaxis().SetTitle("Var")
g.GetYaxis().SetTitle("data-MC ratio")
ip = 0

for ibin in range(1, nbins+1):
    xc = reweight_hist.GetXaxis().GetBinCenter(ibin)
    xcenter.append(xc)
    xbin.append(reweight_hist.GetXaxis().GetBinLowEdge(ibin))

    if reweight_hist.GetBinContent(ibin) == 0: 
        # used for ibin == 1 case
        weights.append(1.)
        continue
    w = data_hist.GetBinContent(ibin) / reweight_hist.GetBinContent(ibin)
    ew = sqrt(  (1/reweight_hist.GetBinContent(ibin))**2 * data_hist.GetBinError(ibin)**2  \
                + ( data_hist.GetBinContent(ibin)/ reweight_hist.GetBinContent(ibin)**2 )**2 * data_hist.GetBinError(ibin)**2)
    weights.append(w)
    errw.append(ew )
    # Fill a TGraph
    g.SetPoint(ip, xc, w )
    g.SetPointError(ip, 0, ew)
    ip+=1

##################################################
# Fit the function
print(">>> Fitting function {}, in range {}".format(args.fit_func, args.fit_range))

# Function is over all the range 
func1 = R.TF1("wf", args.fit_func, xcenter[0], xcenter[-1] )
func1.SetLineWidth(3)
g.Fit("wf", "+","", *args.fit_range)


# Draw the function over the graph
c2 = R.TCanvas()
g.Draw("AP")
func1.Draw("same")
c2.Draw()

########################################################
# Extrapolation and correction

reweight_hist_integral = reweight_hist.Integral()

reweight_hist2 = reweight_hist.Clone()

print('apply weights')
for ibin in range(1, nbins): 
    xc = reweight_hist2.GetBinCenter(ibin)
    corr_fact_extrap = func1.Eval(xc)
    print("X: {:.3f} | corr: {:.3f}".format(xc, corr_fact_extrap))
    bin_content = reweight_hist2.GetBinContent(ibin)
    reweight_hist2.SetBinContent(ibin, bin_content * corr_fact_extrap) 

reweight_hist_integral_new = reweight_hist2.Integral()
integral_ratio = reweight_hist_integral_new / reweight_hist_integral
print(integral_ratio)
log.write("Integral ratio after 1st iteration: {}\n".format(integral_ratio))

# Modify function with factorization 
func2 = R.TF1("wf_norm", "(1/{}) * wf".format(integral_ratio) )

###################################################
# Closure final test

reweight_hist3 = reweight_hist.Clone()

print('apply weights (2nd round)')
for ibin in range(1, nbins): 
    xc = reweight_hist3.GetBinCenter(ibin)
    # use func2
    corr_fact_extrap = func2.Eval(xc)
    print("X: {:.3f} | corr: {:.3f}".format(xc, corr_fact_extrap))
    bin_content = reweight_hist3.GetBinContent(ibin)
    reweight_hist3.SetBinContent(ibin, bin_content * corr_fact_extrap) 

reweight_hist_integral_new = reweight_hist3.Integral()
integral_ratio = reweight_hist_integral_new / reweight_hist_integral
print(integral_ratio)
log.write("Integral ratio after 2st iteration (normalization): {}\n".format(integral_ratio))


c1.cd()
reweight_hist2.Draw("hist same")
reweight_hist2.SetLineColor(R.kOrange)
reweight_hist3.Draw("hist same")
reweight_hist3.SetLineColor(R.kGreen)
leg1.AddEntry(reweight_hist2, args.sample_to_reweight+" reweighted", "l")
leg1.AddEntry(reweight_hist3, args.sample_to_reweight+" reweighted (norm corr)", "l")
c1.Draw()

##################################
#  Ratio plot
h3 = data_hist.Clone("h3")
h3.SetLineColor(R.kBlack)
h3.SetMarkerStyle(21)
h3.SetTitle("")
h3.SetMinimum(0.8)
h3.SetMaximum(1.35)
# Set up plot for markers and errors
h3.Sumw2()
h3.SetStats(0)
h3.Divide(reweight_hist3)

# Adjust y-axis settings
y = h3.GetYaxis()
y.SetTitle("ratio data / mc ")
y.SetNdivisions(505)
y.SetTitleSize(20)
y.SetTitleFont(43)
y.SetTitleOffset(1.55)
y.SetLabelFont(43)
y.SetLabelSize(15)

# Adjust x-axis settings
x = h3.GetXaxis()
x.SetTitleSize(20)
x.SetTitleFont(43)
x.SetTitleOffset(4.0)
x.SetLabelFont(43)
x.SetLabelSize(15)

# def canvas
c3 = R.TCanvas("c3", "canvas", 800, 800)
# Upper histogram plot is pad1
pad1 = R.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0)  # joins upper and lower plot
pad1.SetGridx()
pad1.Draw()
# Lower ratio plot is pad2
c3.cd()  # returns to main canvas before defining pad2
pad2 = R.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
pad2.SetTopMargin(0)  # joins upper and lower plot
pad2.SetBottomMargin(0.2)
pad2.SetGridx()
pad2.Draw()

# draw everything
pad1.cd()
reweight_hist3.Draw()
data_hist.Draw("same")
# to avoid clipping the bottom zero, redraw a small axis
reweight_hist3.GetYaxis().SetLabelSize(0.0)
axis = R.TGaxis(-5, 20, -5, 220, 20, 220, 510, "")
axis.SetLabelFont(43)
axis.SetLabelSize(15)
axis.Draw()
pad2.cd()
h3.Draw("ep")





##################################
# Output file 
outputfile = R.TFile(args.output, "recreate")
func1.Write()
func2.Write()
outputfile.Close()

log.close()

