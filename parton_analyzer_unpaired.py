import ROOT as rt  
import sys  
import utils
import argparse
import os
import multiprocessing
from functools import partial
from contextlib import contextmanager

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def parton_unpaired_to_jets (filename, radius, data_path, nevents, debug):
    file = rt.TFile(data_path + '/' + filename)
    filename = filename[:-5] # remove .root from filename
    tree = file.Get("latino")

    iev = 0
    count_flag2_tot = 0 # number of events that have unpaired partons
    count_flag2_last = 0 # number of events in which the unpaired parton is the last one
    count_flag2_dist = [0.0]*5 

    pt_histo = rt.TH1F('pt', 'Pt ' + filename, 100, 0, 200)
    eta_histo = rt.TH1F('eta', 'Eta ' + filename, 100, 0, 8)
    pt_eta_histo = rt.TH2F('pt_eta', 'Pt Eta ' + filename, 100, 0, 200, 100, 0, 8)
    for event in tree:
        partons, pids = utils.get_hard_partons(event, debug)
        jets = utils.get_jets(event, debug)

        # Remove top events
        if 6 in pids or -6 in pids:
            continue

        if len(partons) != 4:
            print ">>>> Problem! Event not with only 4 partons!!!! <<<<"

        results, flag = utils.associate_vectors(jets, partons, args.radius)
        if flag == 2:
            count_flag2_tot += 1
            # print results
            if results[0][3] == -1:
                # does not have really physical meaning, just a curiosity
                count_flag2_last += 1
            count_flag2_dist[ results[0].count(-1) ] += 1
            unpaired_indices = [i for i, paired in enumerate(results[0]) if paired == -1]
            # print unpaired_indices
            for index in unpaired_indices:
                pt_histo.Fill(partons[index].Pt())
                eta_histo.Fill(abs(partons[index].Eta()))
                pt_eta_histo.Fill(partons[index].Pt(), abs(partons[index].Eta()))
                # print " pt:   ", partons[index].Pt()
                # print " eta: ", partons[index].Eta()

        iev+=1
        if nevents > 0 and iev>= nevents:
            break

    print filename, iev, count_flag2_dist, count_flag2_tot, count_flag2_last

    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    c1 = rt.TCanvas('c1', 'Pt ' + filename, 700, 700)
    pt_histo.Draw()
    # c1.Modified()
    # c1.Update()
    c1.Print('outputs/' + filename + '_unpaired_pt.png', 'png')
    c2 = rt.TCanvas('c2', 'Eta ' + filename, 700, 700)
    eta_histo.SetFillColor(rt.kBlue)
    eta_histo.GetXaxis().SetTitle('eta')
    eta_histo.Draw()
    c2.Print('outputs/' + filename + '_unpaired_eta.png', 'png')
    c3 = rt.TCanvas('c3', 'Pt Eta ' + filename, 700, 700)
    pt_eta_histo.GetXaxis().SetTitle('pt [GeV]')
    pt_eta_histo.GetYaxis().SetTitle('eta')
    pt_eta_histo.Draw('colz')
    c3.Print('outputs/' + filename + '_unpaired_pt_eta.png', 'png')

    out_file = rt.TFile('outputs/' + filename + '_unpaired_out.root', 'RECREATE')
    pt_histo.Write()
    eta_histo.Write()
    pt_eta_histo.Write()
    out_file.Close()

    result='finished'
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parton Analyzer, jet pairing')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    parser.add_argument('--radius', type=float, default=0.8, help="Radius from jet")
    parser.add_argument('--nevents', type=int, default=10, help='How many events per file should be analysed. Set to a negative value to include all events')
    parser.add_argument('--processes', type=int, default=8, help='Number of concurrent processes')
    parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')
    args = parser.parse_args()

    file_list = sorted(os.listdir(args.data_path))
    with poolcontext(processes=args.processes) as pool:
        results = pool.map(partial(parton_unpaired_to_jets, radius=args.radius, data_path=args.data_path, nevents=args.nevents, debug=args.debug), file_list)
