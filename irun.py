from library.models import *
from django.contrib.auth.models import Group
import math,numpy
from scipy import stats
import statistics

# wd=os.getcwd()

# s=open("/Users/gs/Desktop/CL/genes.read_group_tracking","r").read().splitlines()[1:]
# p = Project.objects.get(pk=1)
# u = User.objects.get(username="gs")
# for i in range(len(s)):line=s[i].split('\t');r = read_group_tracking(project=p,tracking_id=line[0],condition=line[1],replicate=line[2],FPKM=line[6],created_by=u);r.save()
# 	s[i]=s[i].replace(",","_").replace(' ','_')
# 	line=s[i].split('\t');r = read_group_tracking(project=p,tracking_id=line[0],condition=line[1],replicate=line[2],FPKM=line[6]);print(vars(r))


# 	tracking_id = models.CharField(max_length=100)
# 	condition = models.CharField(max_length=100)
# 	replicate = models.IntegerField(default=0)
# 	FPKM = models.FloatField(default=0)
# s=open("/Users/gs/Desktop/CL/gene_exp.diff","r").read().splitlines()[1:]
# for v in s:
# # 	line=v.replace(',',"_").split('\t')
# 	line = v.split('\t')
# 	cond=str(line[4]+","+line[5])
# 	cond_1=line[4]
# 	cond_2=line[5]
# 	gene=line[0]
# 	inf=str(line[9])
# 	FC=0.0
# 	PV=float(line[11])
# 	fpkm_1=float(line[7])
# 	fpkm_2=float(line[8])
# 	if "inf" in inf:
# 		inf=True
# 		fpkm_1=fpkm_1+1
# 		fpkm_2=fpkm_2+1
# 		FC=math.log((fpkm_2/fpkm_1),2)
# 	else :FC=float(inf);inf=False;
#
# 	g=gene_exp(created_by=u,inf=inf,test_id=gene,sample_1=cond_1,sample_2=cond_2,p_value=PV,FC=FC,fpkm_1=fpkm_1,fpkm_2=fpkm_2,q_value=line[13],\
# 	SEM_1=stats.sem([ i['FPKM'] for i in read_group_tracking.objects.filter(project=p,tracking_id=gene,condition=cond_1).values('FPKM')]),\
# 	SEM_2=stats.sem([ i['FPKM'] for i in read_group_tracking.objects.filter(project=p,tracking_id=gene,condition=cond_2).values('FPKM')]))
# 	g.save()