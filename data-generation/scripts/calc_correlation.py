"""Runs through output directory of percentile_per_field_breakdown.py and 
calculates correlation between percentile of citations and percentage of 
emails covered. writes to correlations.json"""
import glob, os, json
import numpy as np
outdict={}
for file in glob.glob("*.json"):
    print((file.split('.')[0].split("_")[2:][0]))
    topic=(file.split('.')[0].split("_")[2:][0])
    dict=json.loads(open(file).read().replace('\n',''))
    keys=[float(i) for i in list(dict.keys())]
    values=[float(i) for i in list(dict.values())]
    corr=np.corrcoef(values, keys)
    print((corr[0][1]))
    outdict[topic]=corr[0][1]
outfile=open('correlations.json',"w")
outfile.write(json.dumps(outdict,indent=4))