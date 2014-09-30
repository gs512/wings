#!/usr/bin/env python3
import os
import sys
from urllib.request import urlopen
import json
import os.path
import time

if len(sys.argv) > 1:
	gene_list=sys.argv[1]

if "," in gene_list:
	gene_list=gene_list.split(",")
else: 
	if os.path.isfile(gene_list):gene_list=(open(gene_list,"r").read().splitlines())[1:]
	else: gene_list=[gene_list]

for gene in gene_list:
	gene=gene.split(',')
	tf=""
	prot=""
	# if len(gene)>1:
	# 	prot=(gene[3]).splitlines(';')
	# 	tf=gene[1]
	gene=gene[0]
	# print(gene)
	time.sleep(0.25)
	response = urlopen(("http://grch37.rest.ensembl.org/xrefs/id/{}?content-type=application/json").format(gene))
	data = json.loads(response.read().decode('utf-8'))
	warning = True
	for hit in data:
		if hit['dbname'] == "EntrezGene":
			print(("{},{},{}").format(gene,hit['display_id'],hit['primary_id']));warning=False;
	if warning: print(("{}\tnot found ").format(gene))
	