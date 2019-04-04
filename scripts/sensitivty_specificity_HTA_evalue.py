#!/usr/bin/python

##########################################################################
# Copyright (C) 2017-2018 Michelle Treiber
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation;
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
##########################################################################
#
# sensitivty_specificity_HTA_evalue.py
# Created December 28, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to calculate true positive, false positive, true
# negative, and false negative rates and print to a table in preparation 
# for an ROC curve.
# Script will also calculate specificity, sensitivity, and accuracy
# and create another output table for those results.
#
######################################################################
#
# Usage:
#
# -db		database		Fasta formatted test database containing simulated 
#								metagenome reads
#
# -ref 		reference 		Fasta formatted protein database containing only
#								Homoserine transacetylase
#
# -i		input file		DIAMOND results file
#
# -o1 		output file	1	name of results table containing sensitivity,
#								specificity, and accuracy results 
# 
# -o2 		output file 2	name of results table containing true positive,
#								false positive, true negative, and false 
#								negative results 
#
# Example usage: python sensitivty_specificity_HTA_evalue.py -db 100_test_database.mg.fna -ref db_with_HTA.faa -i 100_test_database.mg.annot_HTA.txt -o1 50rl_sensitivty_specificity_HTA_evalue_extended.txt -o2 50rl_TP_FP_TN_FN_extended.txt
#
##############################################################################

import re
import argparse
import os
from os.path import basename

# create flag arguments:
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", dest = "db", help = "original test database with simulated metagenome reads")
parser.add_argument("-ref", "--reference", dest = "ref", help = "reference database that includes all homoserine-o-acetyltransferase proteins")
parser.add_argument("-i", "--input", dest = "input", help = "DIAMOND results file")
parser.add_argument("-o1", "--output1", dest = "output1", help = "output filename")
parser.add_argument("-o2", "--output2", dest = "output2", help = "output filename")

args = parser.parse_args()
store = vars(args)
count = sum([ 1 for a in store.values( ) if a]) # total number of arguments passed through the command line

# check if there are enough arguments passed
if count != 5:
        print 'ERROR: Too few arguments. Must include input metagenome, reference homoserine-o-acetyltransferase protein database, DIAMOND result, and two output files\nExample usage: python TP_and_FP_rates.py -db 100_test_database.mg.fna -ref db_with_HTA.faa -i 100_test_database.mg.annot_HTA.txt -o1 50rl_sensitivty_specificity_HTA_evalue_extended.txt -o2 50rl_TP_FP_TN_FN_extended.txt'

print("Test database: %s, HTA protein reference database: %s, DIAMOND results file: %s, Output file 1: %s, Output file 2: %s") % (args.db, args.ref, args.input, args.output1, args.output2)

# Set arguments to variables
test_db = args.db
reference = args.ref
diamond_result = args.input
out1 = args.output1
out2 = args.output2

# open output files
outfile1 = open(out1, 'a')
outfile2 = open(out2, 'a')

shortname = basename(diamond_result)
evalue = re.split('[_.]', shortname)[6]
amt = shortname.split('_')[0]
HTA_reads = 350
not_HTA_reads = 100000 - HTA_reads
print "Total number of reads derived from Homoserine O-acetyltransferase in ", shortname, ": ", HTA_reads
print "Total number of reads that were not derived from Homoserine O-acetyltransferase in ", shortname, ": ", not_HTA_reads

# make two lists: one with only HTA IDs, one with all IDs except HTA
test_db_HTA_ids = []
test_db_no_HTA_ids = []
with open(test_db, 'rU') as f:
	for line in f:
		if line.startswith('>'):
			if "Homoserine O-acetyltransferase" in line:
				test_db_HTA_ids.append(re.split('[> |]', line)[1])
			else:
				test_db_no_HTA_ids.append(re.split('[> |]', line)[1])

print "A check to verify that all Homoserine O-acetyltransferase reads are counted for: ",
print len(test_db_HTA_ids) # check to verify that all Homoserine O-acetyltransferase reads are counted for

# Make a reference list of HTA ids from database containing only HTA proteins
# Note: Reference database only necessary if DIAMOND results contain more proteins
# than the protein of interest. For this script it is an optional addition.
reference_HTA_ids = []
with open(reference, "rU") as f:
	for line in f:
		if line.startswith('>'):
			reference_HTA_ids.append(re.split('[> ]', line)[1])
print reference_HTA_ids

# set counters
TP = 0
FP = 0
diamond_HTA_results = []
with open(diamond_result, 'rU') as f:
	for line in f:
		split_line = re.split('[/\t+ ]', line)
		test_db_id = split_line[0]
		prot_db_id = split_line[1]
		if prot_db_id in reference_HTA_ids: # positive result is a read aligning to HTA
			#print prot_db_id
			diamond_HTA_results.append(test_db_id)
			# True positive results are HTA ids that are correctly mapped
			# 	to HTA (in HTA diamond results and are HTA)
			if test_db_id in test_db_HTA_ids:
				TP += 1
			# False positive results are ids that are incorrectly mapped to
			# 	HTA (in HTA diamond results, but are not actually HTA)
			else:
				#print test_db_id
				FP += 1

print len(diamond_HTA_results)
print "True positve result: ", TP
print "False positve result: ", FP

# Find true negative results: any id that is not beta gal and is not mapped
# 	to beta gal (not in the beta gal diamond results)
TN = 0
for id in test_db_no_HTA_ids:
        if id not in diamond_HTA_results:
                TN += 1

# Find false negative results: any id that is beta gal and is not mapped
# 	to beta gal (not in the beta gal diamond results)
FN = 0
for id in test_db_HTA_ids:
        if id not in diamond_HTA_results:
                FN += 1
print "True negative result: ", TN
print "False negative result: ", FN

# Calculate sensitivity, specificity, and accuracy
sensitivity = float(TP) / (TP + FN)
specificity = float(TN) / (FP + TN)
accuracy = float(TP + TN) / 100000

print "sensitivity: ", sensitivity
print "specificity: ", specificity
print "accuracy: ", accuracy

print >> outfile1, evalue,"\t",sensitivity,"\t",specificity,"\t",accuracy
print >> outfile2, evalue,"\t",TP,"\t",FP,"\t",TN,"\t",FN

# close output files
outfile1.close()
outfile2.close()
