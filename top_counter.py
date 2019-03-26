import ROOT as rt  
import sys  
import utils
import os
import argparse
import multiprocessing
from functools import partial
from contextlib import contextmanager


@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def count_t_tbar(f, data_path, nevents, debug):
    file = rt.TFile(data_path + '/' + f)
    tree = file.Get("latino")

    iev = 0
    count_tbar = 0
    count_t = 0
    count_no_t_tbar = 0
    for event in tree:

        # print "> event: ", iev
        partons, pids = utils.get_hard_partons(event, debug)

        # print "partons PID: ", pids
        index_t = -1
        index_tbar = -1
        found_t = False
        found_tbar = False
        try:
            index_t = pids.index(6) 
            found_t = True
        except:
            pass
        try:
            index_tbar = pids.index(-6)
            found_tbar = True
        except:
            pass
        if found_t:
            count_t += 1
        if found_tbar:
            count_tbar +=1
        if (not found_t) and (not found_tbar):
            count_no_t_tbar += 1
        # print index_t, index_tbar

        iev+=1
        if nevents > 0 and iev >= nevents:
            break
    result = [f, iev, count_no_t_tbar, count_t, count_tbar, count_t + count_tbar + count_no_t_tbar - iev]
    print result
    return result

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Count how many t and tbar are present in every event')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    parser.add_argument('--nevents', type=int, default=-1, help='How many events per file should be analysed. Set to a negative value to include all events')
    parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')
    parser.add_argument('--processes', type=int, default=8, help='Number of concurrent processes')
    args = parser.parse_args()

    file_list = sorted(os.listdir(args.data_path))
    print 'file tot_events no_t_no_tbar t tbar t_tbar'
    with poolcontext(processes=args.processes) as pool:
        results = pool.map(partial(count_t_tbar, data_path=args.data_path, nevents=args.nevents, debug=args.debug), file_list)
    print sorted(results)
