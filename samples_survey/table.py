'''
samples_latino: contains `samples` 
* keys are `latino_name`

samples_gdoc: contains `samples_gdoc`
* array of `latino_code`

samples_vbsjjlnu: contains `samples_vbsjjlnu`
* keys are `latino_code`
* elements are array of `latino_name`
'''
import samples_summer16_Feb2017 as samples_latino
import samples_gdoc
import samples_hercules
import samples_vbsjjlnu

from pprint import pprint
import pandas as pd

samples_summary = {}

for latino_code, hercules_sample in samples_gdoc.samples_gdoc.items():
    try:
        # performance
        sample_latino = samples_latino.samples[latino_code]
        samples_summary[latino_code] = {}
        samples_summary[latino_code]['latino_code'] = latino_code 
        samples_summary[latino_code]['latino_name'] = latino_code 
        samples_summary[latino_code]['das_name'] = sample_latino[0]
        samples_summary[latino_code]['transferred'] = hercules_sample['transferred']
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

df = pd.DataFrame.from_dict(data=samples_summary, orient='index')
df = df.reset_index()
df = df.groupby(['latino_code', 'latino_name']).agg({'transferred':'sum', 'vbsjjlnu':'sum', 'das_name': 'first'})
df = df[['transferred', 'vbsjjlnu', 'das_name']]
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
        else:
            output_file.write(line)
