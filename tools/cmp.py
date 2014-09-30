#!/usr/bin/python
import os
import glob
import sys
import string
import re

res={}
	
tmp=open("rep.txt","r").read().splitlines()
for l in tmp:
	l=l.split(',')
	if l[0] not in res:res[l[0]]=float(l[1])
	else: res[l[0]]+=float(l[1])

for i in res:print(i,",",float(res[i])/2)

		