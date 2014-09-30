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

filer=OrderedDict()
# if os.path.exists(wd+"/filter.txt"):
# 	tmp=open(wd+"/filter.txt","r").read().splitlines()
# 	for l in tmp:
# 		t=l.split(',')
# 		if "ATL1" in t[0]:
# 			if '[' in t[0]:print("ATL1 in list")
# 			else: print("ATL1 ALL")
# 		else:
# 			if 
out_line="gene_id"+",Up at least one,Up in all,Up in H only,Up in C only,Up in S only,UP ATL1 IN H and C"
for cond in grp:out_line=out_line+(",{},{},{},{}").format(cond+"_FC",cond+"_PV",cond+"_Pos",cond+"_Neg")
if not do_inf:print(out_line)
inf_line=""

for g in gene_ind:
	tmp_line=""
	inf=False
	tmp_line=""
	for cond in grp:
		if g in grp[cond]:
			if(grp[cond][g][9]).find("inf")>-1:inf=True
# 			print(grp[cond][g][9])
			tmp_line=tmp_line+(",{},{},{},{}").format(grp[cond][g][9],grp[cond][g][11],grp[cond][g][8],grp[cond][g][7])
		else:tmp_line=tmp_line+(",{},{},{},{}").format("","","","")
	
	tmp_l=tmp_line.split(',')
	tmp_l=tmp_l[1:]
	for i in range(len(tmp_l)):
		if tmp_l[i]=='':tmp_l[i]=0
# 	print(tmp_l)
	up_in_one=0
	up_in_all=0
	up_h_only=0
	up_c_only=0
	up_s_only=0
	up_atl1_hc=0
# 	print(g)
# 	tout=""
# 	for i in range(len(tmp_l)):
# 		if i%4==0:
# 			tout=tout+" "+str(tmp_l[i])
# 	print(g+tout,"#",float(tmp_l[12]),float(tmp_l[16]),float(tmp_l[20]))		
	if(float(tmp_l[0])>=1 and float(tmp_l[4])>=1 and float(tmp_l[8])>=1 and float(tmp_l[12])>=1 and float(tmp_l[16])>=1 and float(tmp_l[20])>=1 and float(tmp_l[24])>=1 and float(tmp_l[28])>=1 and float(tmp_l[32])>=1):up_in_all=1;up_in_one=1
	else:
		if(float(tmp_l[0])>=1 or float(tmp_l[4])>=1 or float(tmp_l[8])>=1 or float(tmp_l[12])>=1 or float(tmp_l[16])>=1 or float(tmp_l[20])>=1 or float(tmp_l[24])>=1 or float(tmp_l[28])>=1 or float(tmp_l[32])>=1):up_in_one=1
		if((float(tmp_l[0])>=1 or float(tmp_l[12])>=1 or float(tmp_l[24])>=1 ) and (float(tmp_l[4])<1 and float(tmp_l[16])<1 and float(tmp_l[28])<1 and float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_h_only=1
		if((float(tmp_l[4])>=1 or float(tmp_l[16])>=1 or float(tmp_l[28])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[12])<1 and float(tmp_l[24])<1 and float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_c_only=1
		if( (float(tmp_l[8])>=1 or float(tmp_l[20])>=1 or float(tmp_l[32])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[12])<1 and float(tmp_l[24])<1 and float(tmp_l[4])<1 and float(tmp_l[16])<1 and float(tmp_l[28])<1)):up_s_only=1
		if((float(tmp_l[0])>=1 or float(tmp_l[12])>=1 or float(tmp_l[24])>=1 ) and (float(tmp_l[4])>=1 or float(tmp_l[16])>=1 or float(tmp_l[28])>=1 ) and (float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_atl1_hc=1
		
		
	tmp_line=(g+",{},{},{},{},{},{}"+tmp_line).format(up_in_one,up_in_all,up_h_only,up_c_only,up_s_only,up_atl1_hc)
		
	if not do_inf and not inf: print(tmp_line)
	else: 
		if do_inf and inf :inf_line=inf_line+"\n"+tmp_line


if do_inf:# 	
	print(out_line)
	for g in inf_line[1:].splitlines():
# 		print(g)
		g=g.split(',')
		i=7
		while i<len(g):
			if "inf" in (g[i+0]):
				g[i+0]=str(math.log((float(g[i+2])+1)/(float(g[i+3])+1),2))
				g[i+2]=str(float(g[i+2])+1)
				g[i+3]=str(float(g[i+3])+1)
			i=i+4
# 		print((',').join(g))	
# 		print(g)
		tmp_l=g[7:]
# 		print(len(tmp_l),tmp_l)
		for i in range(len(tmp_l)):
			if tmp_l[i]=='':tmp_l[i]=0
		up_in_one=0
		up_in_all=0
		up_h_only=0
		up_c_only=0
		up_s_only=0
		up_atl1_hc=0
		if(float(tmp_l[0])>=1 and float(tmp_l[4])>=1 and float(tmp_l[8])>=1 and float(tmp_l[12])>=1 and float(tmp_l[16])>=1 and float(tmp_l[20])>=1 and float(tmp_l[24])>=1 and float(tmp_l[28])>=1 and float(tmp_l[32])>=1):up_in_all=1;up_in_one=1
		else:
			if(float(tmp_l[0])>=1 or float(tmp_l[4])>=1 or float(tmp_l[8])>=1 or float(tmp_l[12])>=1 or float(tmp_l[16])>=1 or float(tmp_l[20])>=1 or float(tmp_l[24])>=1 or float(tmp_l[28])>=1 or float(tmp_l[32])>=1):up_in_one=1
			if((float(tmp_l[0])>=1 or float(tmp_l[12])>=1 or float(tmp_l[24])>=1 ) and (float(tmp_l[4])<1 and float(tmp_l[16])<1 and float(tmp_l[28])<1 and float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_h_only=1
			if((float(tmp_l[4])>=1 or float(tmp_l[16])>=1 or float(tmp_l[28])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[12])<1 and float(tmp_l[24])<1 and float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_c_only=1
			if( (float(tmp_l[8])>=1 or float(tmp_l[20])>=1 or float(tmp_l[32])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[12])<1 and float(tmp_l[24])<1 and float(tmp_l[4])<1 and float(tmp_l[16])<1 and float(tmp_l[28])<1)):up_s_only=1
			if((float(tmp_l[0])>=1 or float(tmp_l[12])>=1 or float(tmp_l[24])>=1 ) and (float(tmp_l[4])>=1 or float(tmp_l[16])>=1 or float(tmp_l[28])>=1 ) and (float(tmp_l[8])<1 and float(tmp_l[20])<1 and float(tmp_l[32])<1)):up_atl1_hc=1
		g[1]=str(up_in_one)
		g[2]=str(up_in_all)
		g[3]=str(up_h_only)
		g[4]=str(up_c_only)
		g[5]=str(up_s_only)
		g[6]=str(up_atl1_hc)
		print((',').join(g))	