#!/usr/local/bin/env python3
""""
This file is intended to be a helper script for 
me to hand-label my python scripts with their
classifications. It will tell me the name of a
python file, and as me for a classification. That way,
I should be able to label many many scripts relatively
quickly. 

It should also generate/add to the data file which is generated
"""
import glob
import csv
import pandas as pd

DATA_FILE = "job_labels.csv"

def load_scripts(script_dir="scripts"):
	directory = f"{script_dir}/*.py"
	scripts = glob.glob(directory)
	return scripts

def label_script(script, label):
	with open(DATA_FILE, "a") as fh:
		writer = csv.DictWriter(fh, fieldnames=["file", "class"])
		writer.writerow({"file": script.split("/")[-1], "class": label})

def get_script_data(script):
	type = input(script+"\n"+"cpu, mem, network, io, other\n")
	return script, type

def get_and_write_all():
	scripts = load_scripts()
	df = pd.read_csv(DATA_FILE)
	prev_scripts = df.file
	for s in prev_scripts:
		scripts.remove("scripts/"+s)
	for script1 in scripts:
		if script1.split('/')[-1].strip() not in prev_scripts:
			script, cat = get_script_data(script1)
			label_script(script, cat)

if __name__ == '__main__':
	get_and_write_all()