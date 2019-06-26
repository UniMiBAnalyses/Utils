'''
samples_latino: contains `samples` 
* keys are `latino_name`

samples_gdoc: contains `samples_gdoc`
* keys are `latino_code`
* elements are array of `latino_name`

samples_vbsjjlnu: contains `samples_vbsjjlnu`
* keys are `latino_code`
* elements are array of `latino_name`
'''

import samples_summer16_Feb2017 as samples_latino
import samples_gdoc
import samples_vbsjjlnu

from pprint import pprint
import pandas as pd
import yaml
import os

def check_sample_hercules(latino_name, config, sample_summary):
    if config == None:
        return []
    
    base_bkg_path = config['base_path'] + config['bkg_path']
    latino_name_mask = 'latino_' + latino_name + '__'
    for step in config['bkg_steps']:
        for step_name, step_path in step.items():
            found = False
            for file in os.listdir(base_bkg_path + step_path):
                if file.find(latino_name_mask) == 0:
                    found = True
            # sample_summary[latino_name][step_name] = os.path.isfile(full_bkg_path)
            sample_summary[latino_name][step_name] = found

    return sample_summary

def df_cut_mask(df, cuts):
    cut_mask = True
    for cut in cuts:
        for cut_name, cut_value in cut.items():
            cut_mask = cut_mask & (df[cut_name] == cut_value)
    return cut_mask

if __name__ == '__main__':
    samples_summary = {}

    config = {}
    with open('config.yaml') as f:
        config = yaml.load(f)

    for latino_code, sample_desired in samples_gdoc.samples_gdoc.items():
        latino_name_full = []
        for latino_name in samples_latino.samples.keys():
            if latino_name.find(latino_code) == 0:
                latino_name_full.append(latino_name)
                samples_summary[latino_name] = {}
                samples_summary[latino_name]['latino_code'] = latino_code 
                samples_summary[latino_name]['latino_name'] = latino_name
                samples_summary[latino_name]['das_name'] = samples_latino.samples[latino_name][0]
                for step in config['bkg_steps']:
                    for stepname in step.keys():
                        samples_summary[latino_name][stepname] = False
                        if ('table_columns' in config.keys()) and (not stepname in config['table_columns']):
                            config['table_columns'].append(stepname)

        latino_name_used = []
        if latino_code in samples_vbsjjlnu.samples_vbsjjlnu_bkg.keys():
            for latino_name in samples_vbsjjlnu.samples_vbsjjlnu_bkg[latino_code]['samples']:
                latino_name_used.append(latino_name)

        latino_name_desired = []
        if 'samples' in sample_desired.keys():
            for latino_name in sample_desired['samples']:
                latino_name_desired.append(latino_name)
        elif 'use' in sample_desired.keys() and sample_desired['use'] == True:
            latino_name_desired = latino_name_full

        for latino_name in latino_name_used:
            samples_summary[latino_name]['used'] = True
            samples_summary[latino_name]['desired'] = 'N.A.'
            samples_summary[latino_name]['priority'] = 'N.A.'
            samples_summary = check_sample_hercules(latino_name, config, samples_summary)
        for latino_name in latino_name_desired:
            if not latino_name in latino_name_used:
                samples_summary[latino_name]['used'] = False
                samples_summary[latino_name]['desired'] = True
                samples_summary[latino_name]['priority'] = sample_desired['priority']
                samples_summary = check_sample_hercules(latino_name, config, samples_summary)
        for latino_name in latino_name_full:
            if not latino_name in latino_name_used and not latino_name in latino_name_desired:
                samples_summary[latino_name]['used'] = False
                samples_summary[latino_name]['desired'] = False
                samples_summary[latino_name]['priority'] = 'N.A.'
                samples_summary = check_sample_hercules(latino_name, config, samples_summary)

    df = pd.DataFrame.from_dict(data=samples_summary, orient='index')
    df = df.reset_index()
    df = df.groupby(['latino_code', 'latino_name']).first()
    if 'cut' in config.keys():
        df = df[df_cut_mask(df, config['cut'])]
    if 'table_columns' in config.keys():
        df = df[config['table_columns']]
    pd.set_option('display.max_colwidth', -1)
    with open('samples_nocolor.html', 'w') as f:
        f.write('''<html>
        <head>Samples VBSjjlnu unimib</head>
        <body>''')
        f.write(df.to_html())
        f.write('''</body>
        </html>''')

    # color with green backgroud the True cells
    with open('samples_nocolor.html', 'r') as input_file, open('samples.html', 'w') as output_file:
        for line in input_file:
            if line.strip() == '<td>True</td>':
                output_file.write('<td bgcolor="green">True</td>')
            elif line.strip() == '<td>high</td>':
                output_file.write('<td bgcolor="green">high</td>')
            elif line.strip() == '<td>low</td>':
                output_file.write('<td bgcolor="grey">low</td>')
            else:
                output_file.write(line)


def old_stuff():
    samples_summary = {}

    for latino_code, sample_desired in samples_gdoc.samples_gdoc.items():
        try:
            # performance
            sample_latino = samples_latino.samples[latino_code]
            samples_summary[latino_code] = {}
            samples_summary[latino_code]['latino_code'] = latino_code 
            samples_summary[latino_code]['latino_name'] = latino_code 
            samples_summary[latino_code]['das_name'] = sample_latino[0]
            samples_summary[latino_code]['transferred'] = sample_desired['transferred']
            samples_summary[latino_code]['vbsjjlnu'] = False
            if latino_code in samples_vbsjjlnu.samples_vbsjjlnu_bkg.keys():
                # consisntency check
                if len(samples_vbsjjlnu.samples_vbsjjlnu_bkg[latino_code]['samples']) == 1:
                    samples_summary[latino_code]['vbsjjlnu'] = True
                else:
                    print 'AIUTO'
                    print latino_code
                    print sample_latino
        except:
            found = False
            for key, element in samples_latino.samples.items():
                if key.find(latino_code) == 0:
                    found = True
                    samples_summary[key] = {}
                    samples_summary[key]['latino_code'] = latino_code
                    samples_summary[key]['latino_name'] = key
                    samples_summary[key]['das_name'] = element[0]
                    samples_summary[key]['transferred'] = hercules_sample['transferred']
                    samples_summary[key]['vbsjjlnu'] = False
                    if latino_code in samples_vbsjjlnu.samples_vbsjjlnu_bkg.keys():
                        if key in samples_vbsjjlnu.samples_vbsjjlnu_bkg[latino_code]['samples']:
                            samples_summary[key]['vbsjjlnu'] = True
            if not found:
                samples_summary[latino_code] = {}
                samples_summary[latino_code]['latino_code'] = latino_code
                samples_summary[latino_code]['latino_name'] = 'N.A.'
                samples_summary[latino_code]['das_name'] = 'N.A.'
                samples_summary[latino_code]['transferred'] = hercules_sample['transferred']
                samples_summary[latino_code]['vbsjjlnu'] = False
                if latino_code in samples_vbsjjlnu.samples_vbsjjlnu_bkg.keys():
                    if key in samples_vbsjjlnu.samples_vbsjjlnu_bkg[latino_code]['samples']:
                        samples_summary[latino_code]['vbsjjlnu'] = True
