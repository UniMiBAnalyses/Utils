import ROOT as rt  
import sys  
import utils
import os
import argparse
import multiprocessing
from functools import partial
from contextlib import contextmanager
import pprint
import json

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def jetpairing_ecciciency(file_list, data_path, nevents):
    pairing_result = {
        'file_list': file_list,
        'events': 0,
        'events_notop': 0,
        'events_notop_matched': 0,
        'events_notop_matched_vjets': 0,
        'events_notop_matched_vjets_vbsjets': 0
    }
    for current_file in file_list:
        file = rt.TFile(data_path + '/' + current_file)
        tree = file.Get("latino")

        iev = 0
        for event in tree:
            pairing_result['events'] += 1
            if event.hasTopGen == 0.:
                pairing_result['events_notop'] += 1
            if event.PartonJetMatchFlag == 0:
                pairing_result['events_notop_matched'] += 1
            vjetsmatch   = set([true == reco for true,reco in zip(event.V_jets_true,   event.V_jets)])
            vbsjetsmatch = set([true == reco for true,reco in zip(event.VBS_jets_true, event.VBS_jets)])
            if vjetsmatch == {True}:
                pairing_result['events_notop_matched_vjets'] += 1
            if vjetsmatch == {True} and vbsjetsmatch == {True}:
                pairing_result['events_notop_matched_vjets_vbsjets'] += 1
            iev+=1
            if nevents > 0 and iev>= nevents:
                break
    pairing_result['efficiency_notop_matched_vjets']         = float(pairing_result['events_notop_matched_vjets'])         / float (pairing_result['events_notop_matched'] )
    pairing_result['efficiency_notop_matched_vjets_vbsjets'] = float(pairing_result['events_notop_matched_vjets_vbsjets']) / float (pairing_result['events_notop_matched'] )
    return pairing_result

if __name__ == '__main__':
    '''
    VBSjjlnu:
    python jetpairing_vbsjjlnu_efficiences.py /gwteray/users/govoni/OneLeptonSkims/VBS_semileptonic_signal_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l1tightChain__bvetoTight__LepTrgFix__dorochester__formulasMC__resolvedVBSPairingGenAndVars --nevents -1
    '''
    parser = argparse.ArgumentParser(description='Compute jetpairing efficiencies')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    parser.add_argument('--nevents', type=int, default=1, help='How many events per file should be analysed. Set to a negative value to include all events')
    parser.add_argument('--processes', type=int, default=8, help='Number of concurrent processes')

    args = parser.parse_args()

    file_list = sorted(os.listdir(args.data_path))
    file_maks_set = set()
    for file in file_list:
        file_maks_set.add(file[:file.find('__')])
    file_list_grouped = []
    for file_mask in file_maks_set:
        file_mask_list = []
        for file in file_list:
            if file.find(file_mask) != -1:
                file_mask_list.append(file)
        file_list_grouped.append(file_mask_list)
    # pprint.pprint(file_list_grouped)

    # file_list = ['latino_WmTo2J_ZTo2L__part0.root']
    with poolcontext(processes=args.processes) as pool:
        results = pool.map(partial(jetpairing_ecciciency, data_path=args.data_path, nevents=args.nevents), file_list_grouped)
    pprint.pprint (results)
    with open('../pairing_result.txt', 'w') as result_file:
        json.dump(results, result_file)

