#!/usr/bin/python
import os
import glob
import sys
import string
import re

origin_head=['gene_id','LP2_H_FC','LP2_H_PV','LP2_H_Neg_fpkm','LP2_H_Pos_fpkm','LP2_H_Neg_SEM','LP2_H_Pos_SEM','LP2_C_FC','LP2_C_PV','LP2_C_Neg_fpkm','LP2_C_Pos_fpkm','LP2_C_Neg_SEM','LP2_C_Pos_SEM','LP2_S_FC','LP2_S_PV','LP2_S_Neg_fpkm','LP2_S_Pos_fpkm','LP2_S_Neg_SEM','LP2_S_Pos_SEM','LP7_H_FC','LP7_H_PV','LP7_H_Neg_fpkm','LP7_H_Pos_fpkm','LP7_H_Neg_SEM','LP7_H_Pos_SEM','LP7_C_FC','LP7_C_PV','LP7_C_Neg_fpkm','LP7_C_Pos_fpkm','LP7_C_Neg_SEM','LP7_C_Pos_SEM','LP7_S_FC','LP7_S_PV','LP7_S_Neg_fpkm','LP7_S_Pos_fpkm','LP7_S_Neg_SEM','LP7_S_Pos_SEM','LP15_H_FC','LP15_H_PV','LP15_H_Neg_fpkm','LP15_H_Pos_fpkm','LP15_H_Neg_SEM','LP15_H_Pos_SEM','LP15_C_FC','LP15_C_PV','LP15_C_Neg_fpkm','LP15_C_Pos_fpkm','LP15_C_Neg_SEM','LP15_C_Pos_SEM','LP15_S_FC','LP15_S_PV','LP15_S_Neg_fpkm','LP15_S_Pos_fpkm','LP15_S_Neg_SEM','LP15_S_Pos_SEM','LP2_LP7_H_FC','LP2_LP7_H_PV','LP2_H_Pos_fpkm','LP7_H_Pos_fpkm','LP2_H_Pos_SEM','LP7_H_Pos_SEM','LP2_LP7_C_FC','LP2_LP7_C_PV','LP2_C_Pos_fpkm','LP7_C_Pos_fpkm','LP2_C_Pos_SEM','LP7_C_Pos_SEM','LP2_LP7_S_FC','LP2_LP7_S_PV','LP2_S_Pos_fpkm','LP7_S_Pos_fpkm','LP2_S_Pos_SEM','LP7_S_Pos_SEM','LP7_LP15_H_FC','LP7_LP15_H_PV','LP15_H_Pos_fpkm','LP7_H_Pos_fpkm','LP15_H_Pos_SEM','LP7_H_Pos_SEM','LP7_LP15_C_FC','LP7_LP15_C_PV','LP15_C_Pos_fpkm','LP7_C_Pos_fpkm','LP15_C_Pos_SEM','LP7_C_Pos_SEM','LP7_LP15_S_FC','LP7_LP15_S_PV','LP15_S_Pos_fpkm','LP7_S_Pos_fpkm','LP15_S_Pos_SEM','LP7_S_Pos_SEM','F0','1','All','Hu','Cu','Su','HC','T1','Ht','Ct','St','H1','C1','S1','Hn','Cn','Sn','E','S','A']
to_match_head=['gene_id','LP2_H_Pos_fpkm','LP2_H_Pos_SEM','LP2_H_Neg_fpkm','LP2_H_Neg_SEM','LP2_C_Pos_fpkm','LP2_C_Pos_SEM','LP2_C_Neg_fpkm','LP2_C_Neg_SEM','LP2_S_Pos_fpkm','LP2_S_Pos_SEM','LP2_S_Neg_fpkm','LP2_S_Neg_SEM','LP7_H_Pos_fpkm','LP7_H_Pos_SEM','LP7_H_Neg_fpkm','LP7_H_Neg_SEM','LP7_C_Pos_fpkm','LP7_C_Pos_SEM','LP7_C_Neg_fpkm','LP7_C_Neg_SEM','LP7_S_Pos_fpkm','LP7_S_Pos_SEM','LP7_S_Neg_fpkm','LP7_S_Neg_SEM','LP15_H_Pos_fpkm','LP15_H_Pos_SEM','LP15_H_Neg_fpkm','LP15_H_Neg_SEM','LP15_C_Pos_fpkm','LP15_C_Pos_SEM','LP15_C_Neg_fpkm','LP15_C_Neg_SEM','LP15_S_Pos_fpkm','LP15_S_Pos_SEM','LP15_S_Neg_fpkm','LP15_S_Neg_SEM','LP2_H_FC','LP2_H_PV','LP2_C_FC','LP2_C_PV','LP2_S_FC','LP2_S_PV','LP7_H_FC','LP7_H_PV','LP7_C_FC','LP7_C_PV','LP7_S_FC','LP7_S_PV','LP15_H_FC','LP15_H_PV','LP15_C_FC','LP15_C_PV','LP15_S_FC','LP15_S_PV','LP2_LP7_H_FC','LP2_LP7_H_PV','LP2_LP7_C_FC','LP2_LP7_C_PV','LP2_LP7_S_FC','LP2_LP7_S_PV','LP7_LP15_H_FC','LP7_LP15_H_PV','LP7_LP15_C_FC','LP7_LP15_C_PV','LP7_LP15_S_FC','LP7_LP15_S_PV','F0','1','All','Hu','Cu','Su','HC','T1','Ht','Ct','St','H1','C1','S1','Hn','Cn','Sn','E','S','A']
ordered_header=[]

for h in to_match_head:
	if h in origin_head:
		ordered_header.append("$"+str(1+origin_head.index(h)))
wd=os.getcwd()
myDir=wd
wd="/Users/gs/Desktop/to_check/"
origin="1.csv"
output="rec_1.csv"
stream = os.popen(("awk -F',' '{print "+'\",\"'.join(ordered_header)+"}' "+wd+origin+" > "+wd+output+""))
tmp=open(wd+output,"r").read().splitlines()
res={}
for line in tmp:
	line=line.split(',')
	res[line[0]]=line
tmp=open(wd+"jordane.csv","r").read().splitlines()
for line in tmp:
	line=line.split(',')
	x=res[line[0]]
	g=line[0]
	for i in range(1,len(x)):
		if x[i] != line[i]:
			try:
					c=0.0
					a=float(x[i])
					b= float(line[i])
					if a != b:
						if a!=0:c=b/a
						if not (c<=1.1 and c>=0.98):
							print(g,to_match_head[i],a,b)
			except ValueError:print(g,to_match_head[i],x[i],line[i])
	del(res[g])
print(res)
