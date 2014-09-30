#!/usr/bin/env python3
import os
import sys

all_sig = open("140923_Lhx6-GFP_RNAseq_Allsig.csv","r").read().splitlines()
intersect = open("140929_TF_database_Mouse_all_IDs.csv","r").read().splitlines()

print("gene_ID,TF_flag,TF family,Protein have DBD")

for line in all_sig:
	found = [(s) for s in intersect if line in s]
	
	TF_flag="0"
	gene_ID=line
	# Ensemble_ID=""
	# Entrez_ID=""
	TF_family=""
	Protein_have_DBD=""
	
	if found:
		found=found[0].split(',')
		TF_flag="1"
		# Ensemble_ID=found[1]
		# Entrez_ID=found[2]
		TF_family=found[3]
		Protein_have_DBD=found[4]
	
	print(("{},{},{},{}").format(gene_ID,TF_flag,TF_family,Protein_have_DBD))
	