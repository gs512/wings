#!/usr/bin/python
import os
import glob
import sys
import string
import re
files = []
myDir="./"
for root, dirnames, filenames in os.walk(myDir):
    files.extend(glob.glob(root + "/genes.fpkm_tracking"))

ercc={}
for f in files:
	if "ERCC" in f:
		#idx=re.findall('\d+', f)
		idx=f.split('ERCC')
		idx=idx[0].split('_')
		idx=idx[len(idx)-2]
		if idx.isdigit():
			ercc[str(idx[0])]=f
cut="paste "
lab=""
for i in range(len(ercc)):

	t=ercc[str(i+1)]
	if i==0:cut+=" <(sort %s | cut -f1,10) "%(t)
	else:
		cut+=" <(sort %s | cut -f10) "%(t)

print """
%s
%s
"""% (lab,cut)


# ./ercc_fpkm.py
# ./ercc_count.py
# ./sql.py count.txt fpkm.txt > sql.txt ( ajouter le header ID + condition )
# insert sql