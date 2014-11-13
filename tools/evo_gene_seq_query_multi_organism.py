#!/usr/bin/env python3
import os
import sys
from urllib.request import urlopen
import json

species = "mouse"

if len(sys.argv) > 1:
	gene_list=sys.argv[1]

if "," in gene_list:
	gene_list=gene_list.split(",")
else: gene_list=[gene_list]

for gene in gene_list:
	response = urlopen(("http://mygene.info/v2/query?q={}&species={}&entrezonly=1").format(gene,species))
	data = json.loads(response.read().decode('utf-8'))
	
	warning = True
	for entry in data['hits']:
		if gene.lower() == entry['symbol'].lower():
			print(("{}\thttp://www.ncbi.nlm.nih.gov/gene/{}").format(entry['symbol'],entry['entrezgene']));warning=False

	if warning: print(("{}\tnot found ").format(gene))