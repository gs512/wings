#!/usr/bin/python
import os
import glob
import sys
import string
import re
files = []
myDir="./"
for root, dirnames, filenames in os.walk(myDir):
    files.extend(glob.glob(root + "/accepted_hits.bam"))

ercc={}
for f in files:
# 	print(f)
	if "ERCC" in f:
		idx=list(re.findall('\d+', f))
		idx=f.split('_')
		idx=idx[1:-3]
# 		print(idx)
		if len(idx)>1:
			ercc[str("_".join(idx[1::]))]=f	
		else :ercc[str(idx[1])]=f
cut="paste "
lab=""
ercc=sorted(ercc.items(), key=lambda x: x[1])
# print(len(ercc))
first=True
for i in ercc:
	
	t=i[1]
	t=t.split('_ERCC')
	t=t[0]
	t=t.split('./')
	t=t[1]
	t=t.split('/')
	t=t[0]
	lab+="samtools idxstats %s > %s.txt ;"%(i[1],t)
	if first:cut+=" <(cut -f1,3 %s.txt) "%(t);first=False
	else:
		cut+=" <(cut -f3 %s.txt) "%(t)

print(("{} {}").format(lab,cut))

