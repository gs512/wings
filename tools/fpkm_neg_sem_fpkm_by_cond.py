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


# tmp_FC=dict([(k,all([l[0]>=1.0 for (j,l) in i.items() if "H" in j])) for (k,i) in my_flags.items()])
# dict([(gene,any([abs(condition_value[0])>=1.0 for (condition_key,condition_value) in condition_value_dict.items() ])) for (gene,condition_value_dict) in my_flags.items()])
p_value=0.001
if len(sys.argv)>1:p_value=float(sys.argv[2])
wd=os.getcwd()
myDir=wd
wd="/Users/gs/Desktop/CL"
gene_ind={}
grp=OrderedDict()
glist={}
glist["A"]=open(wd+"/A.csv","r").read().splitlines()
glist["E"]=open(wd+"/E.csv","r").read().splitlines()
glist["S"]=open(wd+"/S.csv","r").read().splitlines()
s=open(wd+"/sem.txt","r").read().splitlines()
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

ord_cmp=OrderedDict()
if os.path.exists(wd+"/ord_cmp.txt"):
	tmp=open(wd+"/ord_cmp.txt","r").read().splitlines()
	for l in tmp:
		ord_cmp[l]={}


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
	fpkm_1=float(line[7])
	fpkm_2=float(line[8])
	if "inf" in inf:
		inf=True
		fpkm_1=fpkm_1+1
		fpkm_2=fpkm_2+1
		FC=math.log((fpkm_2/fpkm_1),2)
# 		print("FFc",fpkm_1,fpkm_2,FC)
	else :FC=float(inf);inf=False;
	if cond not in grp:grp[cond]={}
# 	print(inf)
# 	print("FF",fpkm_1,fpkm_2,FC)
	grp[cond][gene]=OrderedDict((("FC",FC),("PV",PV),(cond_1+"_fpkm",fpkm_1),(cond_2+"_fpkm",fpkm_2),(cond_1+"_SEM",stats.sem(sem[gene][cond_1])),(cond_2+"_SEM",stats.sem(sem[gene][cond_2])),("inf",inf)))

# pp.pprint(grp)

for my_cmp in ord_cmp:
	my_tmp_cmp=my_cmp.split(',')
	my_tmp_cmp=str(my_tmp_cmp[0]+","+my_tmp_cmp[1])
	if my_tmp_cmp in grp:
# 		print(my_cmp,"is_present",grp[my_tmp_cmp])
		ord_cmp[my_cmp]=grp[my_tmp_cmp]
# 		ord_cmp[(my_cmp.split(','))[2]]=grp[my_tmp_cmp]
	else :
		tmp=my_tmp_cmp.split(',')
		cond_1=tmp[1]
		cond_2=tmp[0]
		tmp=tmp[1]+","+tmp[0]
		if tmp in grp:
			for gene in grp[tmp]:
				val=grp[tmp][gene]
				fp_1=val[cond_2+"_fpkm"]
				fp_2=val[cond_1+"_fpkm"]
				if fp_1==0 or fp_2==0:
					if fp_1==0:fp_1=1
					if fp_2==0:fp_2=1
					val["inf"]=True
				FC=math.log((fp_2/fp_1),2)
				val["FC"]=FC
			ord_cmp[my_cmp]=grp[tmp]
# 			ord_cmp[(my_cmp.split(','))[2]]=grp[tmp]

my_flags={}
for gene in sem:
	my_flags[gene]={}
	for my_cmp in ord_cmp:
		my_flags[gene][my_cmp]=[ord_cmp[my_cmp][gene]["FC"],ord_cmp[my_cmp][gene]["PV"],ord_cmp[my_cmp][gene]]
# 		print(gene,my_cmp,abs(ord_cmp[my_cmp][gene]["FC"])>=1.0 and ord_cmp[my_cmp][gene]["PV"]<=p_value)


tmp_FC=dict([(k,any([(abs(l[0])>=1.0 and l[1]<=p_value) for (j,l) in i.items() ])) for (k,i) in my_flags.items()])
atl_1_res=tmp_FC
# pp.pprint(atl_1_res)

for k in atl_1_res:
	if not atl_1_res[k]:del my_flags[k]
tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2])) for (k,i) in my_flags.items()])
atl_1_res=tmp_FC
# pp.pprint(atl_1_res)

tmp_FC=dict([(k,all([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2])) for (k,i) in my_flags.items()])
all_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "H" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
H_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "C" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
C_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "S" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
S_up=tmp_FC

tmp_FC=dict([(k,all([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))>2 and "S" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
S_pos_up=tmp_FC

tmp_FC=dict([(k,all([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))>2 and "C" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
C_pos_up=tmp_FC

tmp_FC=dict([(k,all([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))>2 and "H" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
H_pos_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))>2  ])) for (k,i) in my_flags.items()])
atl_1_pos_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "H" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
atl_1_TPH_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "C" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
atl_1_TPC_up=tmp_FC

tmp_FC=dict([(k,any([(l[0]>=1.0 and l[1]<=p_value) for (j,l) in i.items() if len(((j.split(','))[2]).split('_'))<=2 and "S" in ((j.split(','))[2]) ])) for (k,i) in my_flags.items()])
atl_1_TPS_up=tmp_FC
# for i in my_flags['Sst']:
# 	if "S" in i:
# 		print(i,my_flags['Sst'][i][0])


all_H_neg_fpkm_lower_10={}
all_C_neg_fpkm_lower_10={}
all_S_neg_fpkm_lower_10={}
for (k,v) in my_flags.items():
	# print(v)
	tmp_v_H=[]
	tmp_v_C=[]
	tmp_v_S=[]
	for (l,m) in v.items():
		for (n,o) in (m[2]).items():
			if "H" in n and "Neg" in n and "fpkm" in n:
				tmp_v_H.append(o)
			if "C" in n and "Neg" in n and "fpkm" in n:
				tmp_v_C.append(o)
			if "S" in n and "Neg" in n and "fpkm" in n:
				tmp_v_S.append(o)
	# print(tmp_v_H)
	all_H_neg_fpkm_lower_10[k]=all(float(o)<10 for o in tmp_v_H)
	all_C_neg_fpkm_lower_10[k]=all(float(o)<10 for o in tmp_v_C)
	all_S_neg_fpkm_lower_10[k]=all(float(o)<10 for o in tmp_v_S)



first=True
head=""
for gene in my_flags:
	# print(sem[gene])
	line=""
	H1=0
	C1=0
	S1=0
	Hn=0
	Cn=0
	Sn=0
	if atl_1_TPH_up[gene]:H1=1
	if atl_1_TPC_up[gene]:C1=1
	if atl_1_TPS_up[gene]:S1=1
	if all_H_neg_fpkm_lower_10[gene]:Hn=1
	if all_C_neg_fpkm_lower_10[gene]:Cn=1
	if all_S_neg_fpkm_lower_10[gene]:Sn=1

	inf=False
	T1=0
	up_in_one=0
	if atl_1_res[gene]:up_in_one=1
	up_in_all=0
	if all_up[gene]:up_in_all=1
	up_h_only=0
	if H_up[gene] and not C_up[gene] and not S_up[gene]:up_h_only=1
	up_c_only=0
	if C_up[gene] and not H_up[gene] and not S_up[gene]:up_c_only=1
	up_s_only=0
	if S_up[gene] and not H_up[gene] and not C_up[gene]:up_s_only=1
	up_atl1_hc=0
	if H_up[gene] and C_up[gene] and not S_up[gene]:up_atl1_hc=1
	if atl_1_pos_up[gene]:T1=1
	E=0
	S=0
	A=0
	F=0
	ht=0
	if H_pos_up[gene]:ht=1
	ct=0
	if C_pos_up[gene]:ct=1
	st=0
	if S_pos_up[gene]:st=1
	for my_cmp in ord_cmp:
		v=[str(i) for(k,i) in ord_cmp[my_cmp][gene].items()]
		if not (abs(float(v[0]))>=1 and float(v[1])<=p_value):
			v[0]=""
			v[1]=""
		k=[k for(k,i) in ord_cmp[my_cmp][gene].items()][:-1]
		cond_prefix=(my_cmp.split(","))[2]
		k[0]=cond_prefix+"_"+k[0]
		k[1]=cond_prefix+"_"+k[1]
		if first:head=head+","+(',').join(k)
		line=line+","+(',').join(v[:-1])
# 		print(v)
		if v[-1]=="True":inf=True
	if first:print("gene_id"+head+",F0,1,All,Hu,Cu,Su,HC,T1,Ht,Ct,St,H1,C1,S1,Hn,Cn,Sn,E,S,A");first=False
# 	if first:print("gene_id"+",H1,C1,S1,Hn,Cn,Sn");first=False
	if gene in glist["A"]:A="1"
	if gene in glist["S"]:S="1"
	if gene in glist["E"]:E="1"
	if inf:inf=1
	else: inf=0
	line=(gene+line+",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}").format(inf,up_in_one,up_in_all,up_h_only,up_c_only,up_s_only,up_atl1_hc,T1,ht,ct,st,H1,C1,S1,Hn,Cn,Sn,E,S,A)

	print(line)
