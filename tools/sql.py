#!/usr/bin/python
import os
import sys
import string 

flowcell="JD_B_140123_12_2014-03-12_C3RDGACXX"

f=open(sys.argv[1])
r=f.read()
r=r.split("\n")
f=open(sys.argv[2])
fpkm=f.read()
fpkm=fpkm.split("\n")

l=r[0].split('\t')
l=l[1:]
print l
out=[]
if len(r)!=len(fpkm): print "aouch!"
# print len(r)
# print r
# print fpkm
for i in range(1,len(r)):
	# print fpkm[i]
	if(len(r[i])>1):out.append(r[i].strip()+'\t'+fpkm[i].strip())

# print out
for lines in out: 
	lines=lines.split('\t')
	# print lines
	# print "%s || %s"%(lines[0],lines[len(l)])
	if lines[0]==lines[len(l)+1]:
		for s in range(0,len(l)):
			print "INSERT INTO `ERCC_RC_FPKM`(`id`, `sample_id`, `ERCC_ID`, `RC`, `FPKM`, `flowcell_id`) VALUES ('','{}','{}',{},{},'{}');".format(l[s],lines[0],lines[s+1],lines[s+2+len(l)],flowcell)

	
# 	rc=rc.split(',')
# 	i=0
# 	l[s][0][0]=rc[0]
# 	for s in hrc:
		

