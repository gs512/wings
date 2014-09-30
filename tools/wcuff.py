#!/usr/bin/python
import os
import glob
import sys
import string
import re
files = []
ERCC=False
gref="/home/gas361/ercc/ERCC92"
gtf="/home/gas361/ercc/ERCC92.gtf"
suffix="_ERCC_OUT"
if not ERCC:
	gref="/home/gas361/mm10/genome"
	gtf="/home/gas361/mm10/genes.gtf"
	suffix="_TH_OUT"
	
wd=os.getcwd()
myDir=wd
al={}
grp={}
if os.path.exists(wd+"/bam_lab.txt"):
	tmp=open(wd+"/bam_lab.txt","r").read().splitlines()
	for l in tmp:
		l=l.split(',')
		lab=""
		if not ERCC:lab=l[0].split('_TH')
		else :lab=l[0].split('_ERCC')
		lab=lab[0]
		al[lab]=l[1]
		tgrp=re.split(r'(\d+)', l[1])
		tid=tgrp[len(tgrp)-2]
		tgrp="".join(tgrp[:-2])
		if tgrp not in grp:grp[tgrp]={}
		grp[tgrp][tid]=lab
# 		print(re.findall(r'^\d+$',))
for root, dirnames, filenames in os.walk(myDir):
	files.extend(glob.glob(root + "/accepted_hits.bam"))

ercc={}

for f in files:
# 	print(f)
	if "ERCC" not in f and not ERCC:

		idx=f.split('_TH')
# 		print(idx)
	else:
		if "ERCC" in f and ERCC:
			idx=f.split('_ERCC')
		else :continue
	idx=idx[0].split('/')
# 	print(idx)
	idx=idx[len(idx)-1]
	ercc[idx]=f

bam=""
lab=""
# ercc=sorted(ercc.items(), key=lambda x: x[1])
# grp=sorted(grp.items(), key=lambda x: x[1])
# print(grp)
# print(al)
# print(ercc)
for i in grp:
	lab+=i+","
	for k in grp[i]:
		bam+=ercc[grp[i][k]]+","
	bam=bam[:-1]
	bam+=" "
# 	bam+=i[1]+","
# 	t=i[0]
# 	if t in al:
# 		t=al[t]
# 	lab+=t+","

lab=lab[:-1]
# print(bam)
# print(lab)
# print(wd,gref,gtf,bam,lab)
print(("LAB='{}' BAM='{}' qsub -N cuffdiff -v 'WD={},IDX={},GTF={},LAB,BAM' ~/cuffdiff.pbs").format(lab,bam,wd,gref,gtf))
