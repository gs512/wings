#!/usr/bin/python
import os
import glob
import sys
import string
# gref="/home/gas361/ercc/ERCC92"
# gtf="/home/gas361/ercc/ERCC92.gtf"
ERCC=True
gref="/home/gas361/ercc/ERCC92"
gtf="/home/gas361/ercc/ERCC92.gtf"
suffix="_ERCC_OUT"
if not ERCC:
	gref="/home/gas361/mm10/genome"
	gtf="/home/gas361/mm10/genes.gtf"
	suffix="_TH_OUT"
	
cuff_pbs="~/scripts/cufflinks.pbs"
x=glob.glob('*.fastq.gz')
x.sort()
my_l={}
for files in x:
	f=files.split('_R')
	if f[0] in my_l:
		my_l[f[0]].append(f[1])
	else:
		my_l[f[0]]=[f[1]]

jid=0
fnames=[]
for file in my_l:
	jid+=1
	if len(my_l[file])==1:
		#single
		fq1=file+"_R"+my_l[file][0]
		file=file[:-12]+suffix
		print "th_{0}=` qsub -N {1} -v OUTPUT={1},FQ1={2},IDX={3},GTF={4},WD={5} ~/scripts/tophat.pbs;`".format(jid,file,fq1,gref,gtf,wd)
		
	else:
		#paired
		fq1=file+"_R"+my_l[file][0]
		fq2=file+"_R"+my_l[file][1]
		file=file+suffix
		print "th_{0}=` qsub -N {1} -v OUTPUT={1},FQ1={2},FQ2={3},IDX={4},GTF={5},WD={6} ~/scripts/tophat.pbs;`".format(jid,file,fq1,fq2,gref,gtf,wd)
# 		print "qsub -N {0} -v OUTPUT=CL_{0},BAM={0}/accepted_hits.bam,GTF={1},WD={2} ~/scripts/ercc_cufflinks.pbs;`".format(file,gtf,wd)
# 		fnames.append(file)

# i=0;
# while i< jid:
# 	i+=1
# 	cid=i
# 	print "cl_"+str(cid)+"=` qsub -W depend=afterok:$th_"+str(i)+" -N CL_"+fnames[i-1]+" -v OUTPUT=CL_"+fnames[i-1]+",BAM="+fnames[i-1]+"/accepted_hits.bam,GTF="+gtf+",WD="+wd+" "+cuff_pbs+";`"
#
# i=0
# dp=""
# while i< jid:
# 	i+=1
# 	dp+="depend=afterok:$cl_"+str(i)+","
#
# dp=dp[:-1]
# print "cm =` qsub -W "+dp+" -N CM_"+file+" -v OUTPUT=CM_"+file+",GTF="+gtf+",IDX="+gref+" ~/cuffmerge.pbs`"
# print "qsub -N CD_"+file+" -W depend=afterok:$cm -v OUTPUT=CD_"+file+",IDX="+gref+",WD="+wd+" ~/cuffdiff.pbs"
#
