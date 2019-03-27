import ROOT as rt  
import sys  
import utils
import os
import argparse
import multiprocessing
from functools import partial
from contextlib import contextmanager

rt.gROOT.SetBatch(True)

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def masses(f, mass, data_path, nevents, debug):
    file = rt.TFile(data_path + '/' + f)
    tree = file.Get("latino")

    iev = 0
    c1 = rt.TCanvas('c1', 'Masses ' + str(mass) + ', ' + f, 700, 700)
    mass_histo = rt.TH1F('masses', str(mass) + ', ' + f, 100, 0., 200.)
    for event in tree:
        # print "> event: ", iev
        partons, pids = utils.get_hard_partons(event, debug)
        if 6 in pids or -6 in pids:
            continue
        mass_w = utils.mass_of_nearest_mass_pair(partons, mass)
        # print mass_w
        mass_histo.Fill( mass_w )
        iev+=1
        if nevents > 0 and iev >= nevents:
            break
    mass_histo.Draw()
    # c1.Modified()
    # c1.Update()
    c1.Print(f + '_' + str(mass) + '.png', 'png')
    result='finished'
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot masses of W and Z in dataset')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    parser.add_argument('mass', type=float, help='mass of the particle that is searched for')
    parser.add_argument('--nevents', type=int, default=-1, help='How many events per file should be analysed. Set to a negative value to include all events')
    parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')
    parser.add_argument('--processes', type=int, default=8, help='Number of concurrent processes')
    args = parser.parse_args()

    file_list = sorted(os.listdir(args.data_path))
    with poolcontext(processes=args.processes) as pool:
        results = pool.map(partial(masses, mass=args.mass, data_path=args.data_path, nevents=args.nevents, debug=args.debug), file_list)
    # print sorted(results)
