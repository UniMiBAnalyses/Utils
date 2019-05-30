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
import pandas as pd

@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def jetpairing_ecciciency(file_list, data_path, nevents):
    pairing_algorithm = 'vjets' if data_path.rfind('VjetpairAndVars') != -1 else 'vbsjets'
    file_mask = file_list[0][:file_list[0].find('__')]
    pairing_result = {
        'tag': file_mask,
        'file_list': file_list,
        'events': 0,
        'events_notop': 0,
        'events_notop_matched': 0,
        'events_notop_matched_first': 0,
        'events_notop_matched_second': 0
    }
    first_eff  = rt.TEfficiency ('first'+file_mask, 'Correct first match vjets;mjj vbsjets [GeV];Efficiency', 15, 0, 1200)
    second_eff = rt.TEfficiency ('second'+file_mask, 'Correct both matches;mjj vbsjets [GeV];Efficiency', 15, 0, 1200)
    for current_file in file_list:
        infile = rt.TFile(data_path + '/' + current_file)
        tree = infile.Get("latino")
        iev = 0
        for event in tree:
            vjetsmatch   = set([true == reco for true,reco in zip(event.V_jets_true,   event.V_jets)]) == {True}
            vbsjetsmatch = set([true == reco for true,reco in zip(event.VBS_jets_true, event.VBS_jets)]) == {True}
            pairing_result['events'] += 1
            if event.hasTopGen == 0.:
                pairing_result['events_notop'] += 1
                if event.PartonJetMatchFlag == 0:
                    pairing_result['events_notop_matched'] += 1
                    second_eff.Fill(vjetsmatch and vbsjetsmatch, event.mjj_vbs)
                    if pairing_algorithm == 'vjets':
                        first_eff.Fill(vjetsmatch, event.mjj_vbs)
                    else:
                        first_eff.Fill(vbsjetsmatch, event.mjj_vbs)
                # IL SEGUENTE BLOCCO DEVE STARE QUI, NON SPOSTARE FUORI DA QUESTO IF
                    if pairing_algorithm == 'vjets':
                        if vjetsmatch:
                            pairing_result['events_notop_matched_first'] += 1
                    else:
                        if vbsjetsmatch:
                            pairing_result['events_notop_matched_first'] += 1
                    if vjetsmatch and vbsjetsmatch:
                        pairing_result['events_notop_matched_second'] += 1
            iev+=1
            if nevents > 0 and iev>= nevents:
                break
    pairing_result['efficiency_notop_matched_first']  = float(pairing_result['events_notop_matched_first'])  / float (pairing_result['events_notop_matched'] )
    pairing_result['efficiency_notop_matched_second'] = float(pairing_result['events_notop_matched_second']) / float (pairing_result['events_notop_matched'] )
    outfile = rt.TFile('../' + file_mask + '.root', 'RECREATE')
    first_eff.Write()
    second_eff.Write()
    outfile.Close()
    return pairing_result

def render_as_table(df):
    df['tag'] = df['tag'].apply(lambda x: x[7:])
    df['tag'] = df['tag'].apply(lambda x: x.split('_'))
    df['tag'] = df['tag'].apply(lambda x: str(x[0]) + str(' ' *(8-len(x[0]))) + str(x[1]))
    df = df.rename(columns={'efficiency_notop_matched_first': 'first'})
    df = df.rename(columns={'efficiency_notop_matched_second': 'second'})
    df['first'] = df['first'].round(2)
    df['second'] = df['second'].round(2)
    df = df.set_index('tag')
    df = df.sort_values('second', ascending=False)
    print df[['first', 'second']]

if __name__ == '__main__':
    '''
    VBSjjlnu:
    python jetpairing_vbsjjlnu_efficiences.py /gwteray/users/govoni/OneLeptonSkims/VBS_semileptonic_signal_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l1tightChain__bvetoTight__LepTrgFix__dorochester__formulasMC__formulasMC__gr4JetsSkim__JetPairingGenVBS__VjetpairAndVars --nevents -1

    ACHTUNG! This script expects the full pathname to contain only once the string "VjetpairAndVars" or "VBSjetpairAndVars"
    '''
    parser = argparse.ArgumentParser(description='Compute jetpairing efficiencies')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    parser.add_argument('--nevents', type=int, default=1, help='How many events per file should be analysed. Set to a negative value to include all events')
    parser.add_argument('--processes', type=int, default=8, help='Number of concurrent processes')

    args = parser.parse_args()

    file_list = sorted(os.listdir(args.data_path))
    file_mask_set = set()
    for f in file_list:
        file_mask_set.add(f[:f.find('__')])
    file_list_grouped = []
    for file_mask in file_mask_set:
        file_mask_list = []
        for file in file_list:
            if file.find(file_mask) != -1:
                file_mask_list.append(file)
        file_list_grouped.append(file_mask_list)
    # pprint.pprint(file_list_grouped)

    # file_list = ['latino_WmTo2J_ZTo2L__part0.root']
    with poolcontext(processes=args.processes) as pool:
        results = pool.map(partial(jetpairing_ecciciency, data_path=args.data_path, nevents=args.nevents), file_list_grouped)
    render_as_table(pd.DataFrame(results))
    
    # aggregate cumulative results
    results_aggregated = {
        'events': 0,
        'events_notop': 0,
        'events_notop_matched': 0,
        'events_notop_matched_first': 0,
        'events_notop_matched_second': 0,
        'efficiency_notop_matched_first': 0.0,
        'efficiency_notop_matched_second': 0.0
    }
    for result in results:
        results_aggregated['events'] += result['events']
        results_aggregated['events_notop'] += result['events_notop']
        results_aggregated['events_notop_matched'] += result['events_notop_matched']
        results_aggregated['events_notop_matched_first'] += result['events_notop_matched_first']
        results_aggregated['events_notop_matched_second'] += result['events_notop_matched_second']

    results_aggregated['efficiency_notop_matched_first']  = float(results_aggregated['events_notop_matched_first'])  / float (results_aggregated['events_notop_matched'] )
    results_aggregated['efficiency_notop_matched_second'] = float(results_aggregated['events_notop_matched_second']) / float (results_aggregated['events_notop_matched'] )
    pprint.pprint(results_aggregated)

    with open('../pairing_' + str( args.data_path[args.data_path.rfind('__')+2:] ) + '.json', 'w') as result_file:
        result_combination = {
            'aggregated': results_aggregated,
            'single_process': results
        }
        json.dump(result_combination, result_file)

