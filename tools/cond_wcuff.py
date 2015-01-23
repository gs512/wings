#!/usr/bin/python
import os
import glob
import sys
import string
import re
# from collections import OrderedDict
files = []
gref="/scratch/gas361/GIA/HSAL/GCA_000147195.fa"
gtf="/scratch/gas361/GIA/HSAL/GCA_000147195.gff"

wd=os.getcwd()
myDir=wd
al={}

if os.path.exists(wd+"/"+sys.argv[1]):
	tmp=open(wd+"/"+sys.argv[1],"r").read().splitlines()
	for l in tmp:
		lab='_'.join((l.split(',')[1]).split('_')[:-1])
		if lab not in al:
			al[lab]=[l.split(',')[0]]
		else: al[lab].append(l.split(',')[0])


bam=""
lab=""

for i in al:
	lab+=i+","
	for k in al[i]:
		bam+=k+","
	bam=bam[:-1]
	bam+=" "

output=sys.argv[1]
output=output+"_CD"
lab=lab[:-1]

print(("#!/bin/sh"))
print(("#PBS -V"))
print(("#PBS -l nodes=1:ppn=4,walltime=16:00:00"))
print(("#PBS -M gas361@nyu.edu"))
print(("#PBS -m abe"))
print(("#PBS -q s48"))
print(("#PBS -l mem=32GB"))
print(("module load cufflinks"))
print(("LAB='"+lab+"'"))
print(("BAM='"+bam+"'"))
print(("OUTPUT="+output+""))
print(("WD="+wd+""))
print(("IDX="+gref+""))
print(("GTF="+gtf+""))
print(("cd $WD"))
print(('echo "cuffdiff -o $OUTPUT -b $IDX -p32 -u $GTF -L $LAB $BAM"'))
print(("cuffdiff -o $OUTPUT -b $IDX -p32 -u $GTF -L $LAB $BAM"))
print(("exit 0;"))
