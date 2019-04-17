import sys  
import utils
import os
import argparse
from pprint import pprint
import pandas as pd  

def parse_datacard(directory, cut, events_datacard_filename):
    '''parse the rates from datacard file'''
    filepath = directory + cut + events_datacard_filename
    cut_description = {'cut': cut}
    with open(filepath) as f:
        lines = f.readlines()
        keywords = ['process', 'rate']
        for line in lines:
            for key in keywords:
                if key in line:
                    rate_line = line.split()
                    rate_line.remove(key)
                    if not key in cut_description:
                        cut_description[key] = rate_line
    return cut_description

def efficiency(directory):
    directory += '/datacards/'
    cuts_list = sorted(os.listdir(directory))
    print cuts_list
    events_datacard_filename = '/events/datacard.txt'

    cuts = {}
    for cut in cuts_list:
        cuts[cut] = parse_datacard(directory, cut, events_datacard_filename)
    print cuts
    
    for cut in cuts:
        if cuts[cut] == 'no_cut':
            break
        cuts[cut]['eff'] = []
        for index, rate in enumerate(cuts[cut]['rate']):
            cuts[cut]['eff'].append(float(rate) / float(cuts['no_cut']['rate'][index]))
    pprint(cuts)

    columns = ['cut_name'] + cuts['no_cut']['process'] 
    df = pd.DataFrame(columns=columns)
    i = 0
    for index in cuts:
        row = [index] + cuts[index]['eff']
        df.loc[i] = row
        i += 1
    # df_t = df.T 
    df = df.sort_values(by=['cut_name'])
    round_mask = {}
    for process in cuts['no_cut']['process']:
        round_mask[process] = 2
    print df.round(round_mask)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute btag efficiencies')
    parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
    args = parser.parse_args()

    efficiency(args.data_path)
