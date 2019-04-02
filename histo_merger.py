import ROOT as rt
import os

rt.gROOT.SetBatch(True)

pt_cumulative_histo = rt.TH1F('pt', 'Pt Cumulative', 100, -200, 200)
eta_cumulative_histo = rt.TH1F('eta', 'Eta Cumulative', 100, -10, 10)

files = [file for file in os.listdir('outputs') if (file.find('.root') != -1 and file.find('cumulative') == -1)]
for filename in files:
    print filename
    tfile = rt.TFile('outputs/' + filename)
    pt_histo = tfile.Get('pt')
    pt_cumulative_histo.Add(pt_histo)
    eta_histo = tfile.Get('eta')
    eta_cumulative_histo.Add(eta_histo)
    tfile.Close()

c1 = rt.TCanvas('c1', 'Pt cumulative', 700, 700)
pt_cumulative_histo.Draw()
c1.Print('outputs/unpaired_pt_cumulative.png', 'png')
c2 = rt.TCanvas('c2', 'Eta Cumulative', 700, 700)
eta_cumulative_histo.Draw()
c2.Print('outputs/unpaired_eta_cumulative.png', 'png')