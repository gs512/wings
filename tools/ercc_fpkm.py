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



# for root, dirnames, filenames in os.walk(myDir):
#     files.extend(glob.glob(root + "/genes.fpkm_tracking"))
#
# ercc={}
# first=True
# for f in files:
#     ercc[f]=[x.split('\t')[9] for x in open(f,"r").read().splitlines()]
# gene_id=[x.split('\t')[0] for x in open(files[0],"r").read().splitlines()]
#
# head="gene_id\t"
# for k in ercc: head+=k+"\t"
# print(head)
# for i in range(len(gene_id)):
#     line=gene_id[i]+'\t'
#     for k in ercc:
#         line+=str(ercc[k][i])+'\t'
#     print(line)

# find . -name "accepted_hits.bam" | grep "1st\|2nd" | grep ERCC| while read file ; do  echo "qsub -v WD=$(pwd),GTF=/home/gas361/ercc/ERCC92.gtf,OUTPUT=CL_$(echo $file | sed -e 's/_ERCC_OUT\/accepted_hits.bam//' -e 's/\//_/g' -e 's/._//'),BAM=$file ~/scripts/ercc_cufflinks.pbs" ; done
# find . -name "accepted_hits.bam" | grep "1st\|2nd" | grep ERCC| while read file ; do  echo " samtools index $file " |sh ; done
# ./ercc_fpkm.py
# echo " paste \\ ";find . -name "genes.fpkm_tracking" |sort | while read file; do  echo " <(sort $file | cut -f10) \\" ; done
# ./ercc_count.py
# echo " paste \\ ";find . -name "accepted_hits.bam"|sort  | grep "1st\|2nd" | grep ERCC| while read file ; do  echo " <(samtools idxstats $file | cut -f3)\ " ; done
# remove last line
#find . -name "accepted_hits.bam"|sort  |  grep ERCC| while read file ; do  echo "$(echo $file|cut -d'/' -f2 | sed -e 's/_ERCC_OUT//') " ; done -> add Header
# ./sql.py count.txt fpkm.txt > sql.txt ( ajouter le header ID + condition )
# insert sql