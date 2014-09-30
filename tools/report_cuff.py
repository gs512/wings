#!/usr/bin/python
import os
import glob
import sys
import string
import re
from collections import OrderedDict
import math

do_inf=False
if len(sys.argv)>1:do_inf=True
wd=os.getcwd()
myDir=wd
gene_ind={}
grp=OrderedDict()
if os.path.exists(wd+"/ord_cond.txt"):
	tmp=open(wd+"/ord_cond.txt","r").read().splitlines()
	for l in tmp:
		if l not in grp:
			grp[l]={}
			val=open(wd+"/tcsv/"+l+".tcsv.csv","r").read().splitlines()
			for v in val:
				line=v.replace(',',"_").split('\t')
				grp[l][line[0]]=line
				if line[0] not in gene_ind:gene_ind[line[0]]=""
				
out_line="gene_id"

for cond in grp:out_line=out_line+(",{},{},{},{}").format(cond+"_FC",cond+"_PV",cond+"_Pos",cond+"_Neg")
print(out_line)
inf_line=out_line

for g in gene_ind:
	tmp_line=""
	inf=False
	tmp_line=g
	for cond in grp:
		if g in grp[cond]:
			if(grp[cond][g][9]).find("inf")>-1:inf=True
# 			print(grp[cond][g][9])
			tmp_line=tmp_line+(",{},{},{},{}").format(grp[cond][g][9],grp[cond][g][11],grp[cond][g][8],grp[cond][g][7])
		else:tmp_line=tmp_line+(",{},{},{},{}").format("","","","")
		
	if not do_inf and not inf: print(tmp_line)
	else: 
		if do_inf and inf :inf_line=inf_line+"\n"+tmp_line


if do_inf:# 	print(g)
	for g in inf_line.splitlines():
		g=g.split(',')
		i=1
		while i<len(g):
			if "inf" in (g[i+0]):
				g[i+0]=str(math.log((float(g[i+2])+1)/(float(g[i+3])+1),2))
				g[i+2]=str(float(g[i+2])+1)
				g[i+3]=str(float(g[i+3])+1)
			i=i+4
		print((',').join(g))	