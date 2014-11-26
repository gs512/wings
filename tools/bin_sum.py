#!/usr/bin/python
import os
import glob
import sys
import string
import re

wd=os.getcwd()
myDir=wd
wd="/Users/gs/Desktop/to_check"
res={}
tmp=open(wd+"/1.csv","r").read().splitlines()
for line in tmp:
	line=line.split(',')
	x=0
	for i in line:x+=int.from_bytes(i.encode(), 'big')
	res[line[0]]=x
tmp=open(wd+"/jordane.csv","r").read().splitlines()
for line in tmp:
	line=line.split(',')
	x=0
	for i in line:x+=int.from_bytes(i.encode(), 'big')
	if res[line[0]]!=x:print(line[0],res[line[0]],x)

