#!/usr/bin/python
import os
import glob
import sys
import string
import re
from collections import OrderedDict
import math,numpy
from scipy import stats
import statistics
import pprint


wd=os.getcwd()
myDir=wd
# wd="/Users/gs/Desktop/CL"
gene_ind={}
grp=OrderedDict()
s=open(wd+"/genes.read_group_tracking","r").read().splitlines()
for i in range(len(s)):
	my=s[i].split('\t')[0:3]
	my.append(s[i].split('\t')[6])
	s[i]='\t'.join(my)
sem={}

replicates=3
pp = pprint.PrettyPrinter(indent=1)


for line in s[1:]:
	line=line.split('\t')
	gene=line[0]
	cond=line[1]
	fpkm=line[3]
	if gene not in sem:sem[gene]={}
	if cond not in sem[gene]:sem[gene][cond]=[];sem[gene][cond].append(float(fpkm))
	else :sem[gene][cond].append(float(fpkm))

val=open(wd+"/gene_exp.diff","r").read().splitlines()
for v in val[1:]:
	line=v.replace(',',"_").split('\t')
	cond=str(line[4]+","+line[5])
	cond_1=line[4]
	cond_2=line[5]
	gene=line[0]
	inf=str(line[9])
	FC=0.0
	PV=float(line[11])
	QV=float(line[12])
	fpkm_1=float(line[7])
	fpkm_2=float(line[8])
	if "inf" in inf:
		inf=1
		fpkm_1=fpkm_1+1
		fpkm_2=fpkm_2+1
		FC=math.log((fpkm_2/fpkm_1),2)
	else :FC=float(inf);inf=0;
	print(("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}").format(gene,cond_1,cond_2,fpkm_1,fpkm_2,stats.sem(sem[gene][cond_1]),stats.sem(sem[gene][cond_2]),FC,PV,QV,inf))

# python3 data_local_infile > ins_in.txt
# LOAD DATA local INFILE '/home/gas361/wings/tools/ins_in.txt' INTO TABLE ins_library_gene_exp (`test_id`, `sample_1`, `sample_2`,`fpkm_1`, `fpkm_2`,`SEM_1`, `SEM_2`,`FC`, `p_value`, `q_value`, `inf`);
# UPDATE `ins_library_gene_exp` SET `created_at`=NOW(),`uuid`=UUID(),`is_locked`=0,`last_modified`=NOW() WHERE 1


