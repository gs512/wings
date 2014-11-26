import math,numpy
from scipy import stats
import statistics

s=open("inf.sql","r").read().splitlines()
for v in s:
 v=v.split(',')
 inf=v[12]
 fpkm_1=float((v[13]))
 fpkm_2=float((v[14]).split(')')[0])
 fpkm_1=fpkm_1+1;fpkm_2=fpkm_2+1;inf=math.log((fpkm_2/fpkm_1),2)
 v[12]=str(inf)
 v[13]=str(fpkm_1)
 v[14]=str(fpkm_2)+");"
 print(','.join(v))
