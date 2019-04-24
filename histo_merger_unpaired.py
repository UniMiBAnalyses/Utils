import ROOT as rt
import os

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)

pt_cumulative_histo = rt.TH1F('pt', 'Pt patrons not paired to any jet', 100, 0, 200)
eta_cumulative_histo = rt.TH1F('eta', 'Eta partons not paired to any jet', 100, 0, 8)
pt_eta_cumulative_histo = rt.TH2F('pt_eta', 'Eta vs Pt partons not paired to any jet', 100, 0, 200, 100, 0, 8)

files = [file for file in os.listdir('outputs') if (file.find('.root') != -1 and file.find('cumulative') == -1)]
for filename in files:
    print filename
    tfile = rt.TFile('outputs/' + filename)
    pt_histo = tfile.Get('pt')
    pt_cumulative_histo.Add(pt_histo)
    eta_histo = tfile.Get('eta')
    eta_cumulative_histo.Add(eta_histo)
    pt_eta_histo = tfile.Get('pt_eta')
    pt_eta_cumulative_histo.Add(pt_eta_histo)
    tfile.Close()

c1 = rt.TCanvas('c1', 'Pt cumulative', 700, 700)
pt_cumulative_histo.SetFillColor(rt.kBlue)
pt_cumulative_histo.GetXaxis().SetTitle('pt [GeV]')
pt_cumulative_histo.Draw()
c1.Print('outputs/unpaired_pt_cumulative.png', 'png')

c2 = rt.TCanvas('c2', 'Eta Cumulative', 700, 700)
eta_cumulative_histo.SetFillColor(rt.kBlue)
eta_cumulative_histo.GetXaxis().SetTitle('eta')
eta_cumulative_histo.Draw()
c2.Print('outputs/unpaired_eta_cumulative.png', 'png')

c3 = rt.TCanvas('c3', 'Pt Eta cumulative', 700, 700)
pt_eta_cumulative_histo.GetXaxis().SetTitle('pt [GeV]')
pt_eta_cumulative_histo.GetYaxis().SetTitle('eta')
pt_eta_cumulative_histo.Draw('colz')
c3.Print('outputs/unpaired_pt_eta_cumulative.png', 'png')