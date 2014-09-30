#!/usr/bin/env python3
import os
import sys
from urllib.request import urlopen
import json

myFile = open("140923_Lhx6-GFP_RNAseq_Allsig.csv","r").read().splitlines()
species = "mouse"

for gene in myFile:
	response = urlopen(("http://mygene.info/v2/query?q={}&species={}&entrezonly=1").format(gene,species))
	data = json.loads(response.read().decode('utf-8'))
	
	warning = True
	for entry in data['hits']:
		if gene.lower() == entry['symbol'].lower():
			print(("{}\thttp://www.ncbi.nlm.nih.gov/gene/{}").format(entry['symbol'],entry['entrezgene']));warning=False

	if warning: print(("{}\tnot found ").format(gene))