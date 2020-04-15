'''
Ratio normalized( Data ) / normalized( MC )


'''

import ROOT as R
import sys
import argparse
from math import sqrt


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, help="mkShape rootFile")
parser.add_argument("--output", type=str, help="Path to file containing the ratios")
parser.add_argument("--var",type=str, help="Variable whose disrtibution is used to compute the new set of weights")
parser.add_argument("--samples",nargs="+", type=str, help="Samples (space-separated list)")
parser.add_argument("--sample-to-reweight",type=str, help="Sample to be reweighted")
parser.add_argument("--cat", type=str, help="Category (only a single category is considered!)")
args = parser.parse_args()

file = args.file
samples = args.samples
cat = args.cat

f = R.TFile(file)

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

c = R.TCanvas()
reweight_hist.Draw("hist")
reweight_hist.SetLineColor(R.kRed)
data_hist.Draw("hist same")
c.Draw()

nbins = data_hist.GetNbinsX()

weights = []
x = []
errw = []
gr = R.TGraphErrors()


for ibin in range(1, nbins+1):
    x.append(reweight_hist.GetXaxis().GetBinLowEdge(ibin))
    if reweight_hist.GetBinContent(ibin) == 0: 
        # used for ibin == 1 case
        weights.append(1.)
        continue
    
    w = data_hist.GetBinContent(ibin) / reweight_hist.GetBinContent(ibin)
    weights.append(w)
    gr.SetPoint(ibin, data_hist.GetBinCenter(ibin), w)

    e = sqrt(  (1/reweight_hist.GetBinContent(ibin))**2 * data_hist.GetBinError(ibin)**2  \
                + ( data_hist.GetBinContent(ibin)/ reweight_hist.GetBinContent(ibin)**2 )**2 * reweight_hist.GetBinError(ibin)**2)
    errw.append( e)
    gr.SetPointError(ibin, 0., e)



#wsum = sum(weights)
#norm_weights = [w / wsum for w in weights]

# with open(args.output , "w") as out:
#     for x,w,err in zip(x,weights, errw):
#         out.write("{:.0f} {} 0. {}\n".format(x,w, err)) 

outfile = R.TFile(args.output , "RECREATE")
gr.SetName("weights")
gr.Write()
outfile.Write()
outfile.Close()