#!/usr/bin/python
import os
import glob
import sys
import string
import re
from collections import OrderedDict
files = []
ERCC=False
gref="/home/gas361/ercc/ERCC92"
gtf="/home/gas361/ercc/ERCC92.gtf"
suffix="_ERCC_OUT"
if not ERCC:
	gref="/home/gas361/mm10/genome.fa"
	gtf="/home/gas361/mm10/genes.gtf"
	suffix="_TH_OUT"
	
wd=os.getcwd()
myDir=wd
al={}
grp=OrderedDict()
if os.path.exists(wd+"/"+sys.argv[1]):
	tmp=open(wd+"/"+sys.argv[1],"r").read().splitlines()
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
		if tgrp not in grp:grp[tgrp]=OrderedDict()
		grp[tgrp][tid]=lab
for root, dirnames, filenames in os.walk(myDir):
	files.extend(glob.glob(root + "/accepted_hits.bam"))

ercc={}

for f in files:

	if "ERCC" not in f and not ERCC:

		idx=f.split('_TH')

	else:
		if "ERCC" in f and ERCC:
			idx=f.split('_ERCC')
		else :continue
	idx=idx[0].split('/')

	idx=idx[len(idx)-1]
	ercc[idx]=f

bam=""
lab=""
# print(sorted(grp,reverse=False))
for i in sorted(grp,reverse=False):
	lab+=i+","
	for k in sorted(grp[i]):
		bam+=ercc[grp[i][k]]+","
	bam=bam[:-1]
	bam+=" "

output=sys.argv[1]
output=output+"_CD"
lab=lab[:-1]
print(("""
#!/bin/sh
#PBS -V
#PBS -l nodes=1:ppn=4,walltime=8:00:00
#PBS -M gas361@nyu.edu
#PBS -m abe
#PBS -q s48
#PBS -l mem=16GB
module load cufflinks
LAB='{}' 
BAM='{}'
OUTPUT={}
WD={}
IDX={}
GTF={}
cd $WD
echo "cuffdiff -o $OUTPUT -b $IDX -p32 -u $GTF -L $LAB $BAM"
cuffdiff -o $OUTPUT -b $IDX -p32 -u $GTF $BAM
exit 0;
""").format(lab,bam,output,wd,gref,gtf))
