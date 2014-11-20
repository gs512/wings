from library.models import *
from django.contrib.auth.models import Group

# wd=os.getcwd()

s=open("/Users/gs/Desktop/CL/genes.read_group_tracking","r").read().splitlines()[1:]
p = Project.objects.get(pk=1)

for i in range(len(s)):line=s[i].split('\t');r = read_group_tracking(project=p,tracking_id=line[0],condition=line[1],replicate=line[2],FPKM=line[6]);print(vars(r));r.save()
# 	s[i]=s[i].replace(",","_").replace(' ','_')
# 	line=s[i].split('\t');r = read_group_tracking(project=p,tracking_id=line[0],condition=line[1],replicate=line[2],FPKM=line[6]);print(vars(r))


# 	tracking_id = models.CharField(max_length=100)
# 	condition = models.CharField(max_length=100)
# 	replicate = models.IntegerField(default=0)
# 	FPKM = models.FloatField(default=0)