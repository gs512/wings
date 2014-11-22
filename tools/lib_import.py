#!/usr/bin/env python3
import os
import sys
import json


myFile = open("/Users/gs/Desktop/w.tsv","r").read().splitlines()

for line in myFile:
	line=line.replace(',','').replace("\t\t","\t").split("\t")
	print((("""l=Library(
	name = "{}",
	library_id = "{}",
	reads_type = "{}",
	flowcell_id = "{}",
	determined_reads = {},
	average_phred = {},
	qc_report_url = "{}",
	ercc_r2 = {},
	ercc_mix = {},
	ercc_dilution = {},
	reads_mapped_refseq_portion = {},
	reads_mapped_ercc = {},
	reads_mapped_ercc_portion = {},
	n = {},
	ercc_url = "{}",
	library_alias = "{}",
	reads_mapped_refseq = {},
	lld = {},
	replicate = {}
);l.save();""").format(line[0],line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[22],line[23])).replace('\n','').replace('\t',''))