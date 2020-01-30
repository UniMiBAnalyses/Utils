'''

'''

import ROOT as R 
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="Input File (output of `reweight_ratiodatamc.py`)")
parser.add_argument("--constscale", type=str, help="Constant scale factor File (output of `reweight_closure.py`)")
parser.add_argument("--output", type=str, help="Output File: Unsafe normalization weights")
parser.add_argument("--output_scaled", type=str, help="Output File: Correct normalization weights")
args = parser.parse_args()


c1 = R.TCanvas( 'c1', 'rew', 0, 60, 800, 600 )
g = R.TGraphErrors()
g.SetTitle("data-MC ratio")
g.SetMarkerStyle(7)
g.SetMarkerSize(3)
g.GetXaxis().SetTitle("Var")
g.GetYaxis().SetTitle("data-MC ratio")
#g.GetYaxis().SetRangeUser(0,200)
g.Draw("AP")

bins = []
xs = []
ys = []
i = 0
deltax = 0.1
with open(args.input) as inputfile:
    ls = inputfile.readlines()
    for l in ls:
        data = list(map(float,l.split(" ")))
        x = data[0]
        y = data[1]
        errx = data[2]
        erry = data[3]
        # using the bin center for the fit
        g.SetPoint(i, x+deltax, y)
        g.SetPointError(i,  errx, erry)
        i+=1
        xs.append(x+deltax)
        bins.append(x)
        print(l)


ranges=[(2,8)]

func1 = R.TF1("wf1", "pol5", ranges[0][0], ranges[0][1])
func1.SetLineWidth(3)
g.Fit("wf1", "+","", ranges[0][0], ranges[0][1])
func_extrapolate = func1.Clone()
func_extrapolate.SetRange(0,100)
func_extrapolate.SetLineStyle(9)
func_extrapolate.SetLineWidth(3)
func_extrapolate.Draw("same")


# estrapolate from 0 to 100
ys = []

for x  in xs:
    ys.append(func1.Eval(x))

with open(args.output, "w") as out:
    for x,y in zip(bins, ys):
        out.write("{:.4f} {}\n".format(x,y)) 

try:
    with open(args.constscale, 'r') as f:
        k = float( f.read() )
    print ("const scale factor for normalization: " + str(k))
    ys = [y / k for y in ys]

    with open(args.output_scaled, "w") as out:
        for x,y in zip(bins, ys):
            out.write("{} {}\n".format(x,y)) 
except Exception as e:
    print ("Not saved correctly-normalized weights: " + str(e))


