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

# do_inf=False
# if len(sys.argv)>1:do_inf=True
wd=os.getcwd()
myDir=wd
gene_ind={}
grp=OrderedDict()
glist={}
glist["A"]=open(wd+"/A.csv","r").read().splitlines()
glist["E"]=open(wd+"/E.csv","r").read().splitlines()
glist["S"]=open(wd+"/S.csv","r").read().splitlines()
s=open(wd+"/sem.txt","r").read().splitlines()
sem={}
replicates=3
for line in s[1:]: 
	line=line.split('\t')
	gene=line[0]
	cond=line[1]
# 	rep=line[2]
	fpkm=line[3]
# 	print(fpkm)
	if gene not in sem:sem[gene]={}
	if cond not in sem[gene]:sem[gene][cond]=[];sem[gene][cond].append(float(fpkm))
	else :sem[gene][cond].append(float(fpkm))

if os.path.exists(wd+"/ord_cond.txt"):
	tmp=open(wd+"/ord_cond.txt","r").read().splitlines()
	for l in tmp:
		if l not in grp:
			grp[l]={}
			if "!" not in l:
				val=open(wd+"/"+l+".tcsv.csv","r").read().splitlines()
			else:val=open(wd+"/"+l[:-1]+".tcsv.csv","r").read().splitlines()
			for v in val:
				line=v.replace(',',"_").split('\t')
				grp[l][line[0]]=line
				if line[0] not in gene_ind:gene_ind[line[0]]=""

filer=OrderedDict()
out_line="gene_id"+",Up at least one,Up in all,Up in H only,Up in C only,Up in S only,UP ATL1 IN H and C,E,S,A,F0"
for cond in grp:
# 	if len(cond.split('_'))<3:
	out_line=out_line+(",{},{},{},{},{},{}").format(cond+"_FC",cond+"_PV",cond+"_Pos",cond+"_Neg",cond+"_Pos_SEM",cond+"_Neg_SEM")
# 	else:
# 		out_line=out_line+(",{},{}").format(cond+"_FC",cond+"_PV")
	
print(out_line+",Ht,Ct,St")
inf_line=""

for g in gene_ind:
	tmp_line=""
	inf=False
	tmp_line=""
	F="0"
	for cond in grp:
# 		print(cond)
		if g in grp[cond]:
			if(grp[cond][g][9]).find("inf")>-1:inf=True;F="1"
			if "!" in cond:
				if not grp[cond][g][8]=="0":
					tmp_FC=float(grp[cond][g][7])/float(grp[cond][g][8])
					if(float(grp[cond][g][7])>0):
						tmp_FC=math.log(tmp_FC,2)
					tmp_FC=str(tmp_FC)
					tmp_line=tmp_line+(",{},{},{},{},{},{}").format(tmp_FC,grp[cond][g][11],grp[cond][g][8],grp[cond][g][7],'','')
				else : 
					inf=True;F="1"
					grp[cond][g][9]="inf"
					tmp_line=tmp_line+(",{},{},{},{},{},{}").format(grp[cond][g][9],grp[cond][g][11],grp[cond][g][7],grp[cond][g][8],'','')
			else:
				if len(cond.split('_'))<3:
					tmp_line=tmp_line+(",{},{},{},{},{},{}").format(grp[cond][g][9],grp[cond][g][11],grp[cond][g][8],grp[cond][g][7],stats.sem(sem[g][cond+"_Pos"]),stats.sem(sem[g][cond+"_Neg"]))
				else:
					tmp_line=tmp_line+(",{},{},{},{},{},{}").format(grp[cond][g][9],grp[cond][g][11],grp[cond][g][8],grp[cond][g][7],'','')			
		else:tmp_line=tmp_line+(",{},{},{},{},{},{}").format("","","","","","")
	
	
	tmp_l=tmp_line.split(',')
	tmp_l=tmp_l[1:]
	tmp_line=tmp_line.split(',')
	for i in range(len(tmp_l)):
		if tmp_l[i]=='':tmp_l[i]=0
	for i in range(len(tmp_l)):
		if str(tmp_l[i]).find("inf")>-1:
			tmp_l[i]=str(math.log((float(tmp_l[i+2])+1)/(float(tmp_l[i+3])+1),2))
			tmp_line[i+1]=tmp_l[i]
			tmp_l[i+2]=str(float(tmp_l[i+2])+1)
			tmp_line[i+2+1]=tmp_l[i+2]
			tmp_l[i+3]=str(float(tmp_l[i+3])+1)
			tmp_line[i+1+3]=tmp_l[i+3]
	tmp_line=(',').join(tmp_line)
	
	
	up_in_one=0
	up_in_all=0
	up_h_only=0
	up_c_only=0
	up_s_only=0
	up_atl1_hc=0
	A="0"
	S="0"
	E="0"
	ht="0"
	ct="0"
	st="0"
#adapt index increment to match the #of values with the SEM elemets

	if(float(tmp_l[0])>=1 and float(tmp_l[6])>=1 and float(tmp_l[12])>=1 and float(tmp_l[18])>=1 and float(tmp_l[24])>=1 and float(tmp_l[30])>=1 and float(tmp_l[36])>=1 and float(tmp_l[42])>=1 and float(tmp_l[48])>=1):up_in_all=1;up_in_one=1
	else:
		if(float(tmp_l[0])>=1 or float(tmp_l[6])>=1 or float(tmp_l[12])>=1 or float(tmp_l[18])>=1 or float(tmp_l[24])>=1 or float(tmp_l[30])>=1 or float(tmp_l[36])>=1 or float(tmp_l[42])>=1 or float(tmp_l[48])>=1):up_in_one=1
		if((float(tmp_l[0])>=1 or float(tmp_l[18])>=1 or float(tmp_l[36])>=1 ) and (float(tmp_l[6])<1 and float(tmp_l[24])<1 and float(tmp_l[42])<1 and float(tmp_l[12])<1 and float(tmp_l[30])<1 and float(tmp_l[48])<1)):up_h_only=1
		if((float(tmp_l[6])>=1 or float(tmp_l[24])>=1 or float(tmp_l[42])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[18])<1 and float(tmp_l[36])<1 and float(tmp_l[12])<1 and float(tmp_l[30])<1 and float(tmp_l[48])<1)):up_c_only=1
		if( (float(tmp_l[12])>=1 or float(tmp_l[30])>=1 or float(tmp_l[48])>=1 ) and (float(tmp_l[0])<1 and float(tmp_l[18])<1 and float(tmp_l[36])<1 and float(tmp_l[6])<1 and float(tmp_l[24])<1 and float(tmp_l[42])<1)):up_s_only=1
		if((float(tmp_l[0])>=1 or float(tmp_l[18])>=1 or float(tmp_l[36])>=1 ) and (float(tmp_l[6])>=1 or float(tmp_l[24])>=1 or float(tmp_l[42])>=1 ) and (float(tmp_l[12])<1 and float(tmp_l[30])<1 and float(tmp_l[48])<1)):up_atl1_hc=1
	if(float(tmp_l[54])>=1 and float(tmp_l[72])>=1):ht="1"
	if(float(tmp_l[60])>=1 and float(tmp_l[78])>=1):ct="1"
	if(float(tmp_l[66])>=1 and float(tmp_l[84])>=1):st="1"
	
	if g in glist["A"]:A="1"	
	if g in glist["S"]:S="1"
	if g in glist["E"]:E="1"
	
	tmp_line=(g+",{},{},{},{},{},{},{},{},{},{}"+tmp_line+",{},{},{}").format(up_in_one,up_in_all,up_h_only,up_c_only,up_s_only,up_atl1_hc,E,S,A,F,ht,ct,st)
# 	print(len(tmp_line.split(',')))
	print(tmp_line)
