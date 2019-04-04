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
# sensitivty_specificity_beta_gal_evalue.py
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
# -i		input file		DIAMOND results file
#
# -o1 		output file	1	name of results table containing sensitivity,
#								specificity, and accuracy results 
# 
# -o2 		output file 2	name of results table containing true positive,
#								false positive, true negative, and false 
#								negative results 
#
# Example usage: python sensitivty_specificity_beta_gal_evalue.py -db 100_test_database.mg.fna -i 100_test_database.mg.annot_BGALAC_1e-3.txt -o1 100rl_sensitivty_specificity_bgal_evalue_extended.txt -o2 100rl_TP_FP_TN_FN_bgal_evalue_extended.txt
#
##############################################################################

import re
import argparse
import os
from os.path import basename

# create flag arguments:
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", dest = "db", help = "original test database with simulated metagenome reads")
parser.add_argument("-i", "--input", dest = "input", help = "DIAMOND results file")
parser.add_argument("-o1", "--output1", dest = "output1", help = "output filename")
parser.add_argument("-o2", "--output2", dest = "output2", help = "output filename")

args = parser.parse_args()
store = vars(args)
count = sum([ 1 for a in store.values( ) if a]) # total number of arguments passed through the command line

# check if there are enough arguments passed
if count != 4:
        print 'ERROR: Too few arguments. Must include pathway abd two output files\nExample usage: python RefSeq_b-galac_inclusive_counter.py -path $starting_files_location/step_2_aggregation_output/refseq_results -out1 b-galac_counts.table.txt -out2 b-galac_percentage.table.txt'

print("Test database: %s, DIAMOND results file: %s, Output files: %s, %s") % (args.db, args.input, args.output1, args.output2)

# Set arguments to variables
test_db = args.db
diamond_result = args.input
out1 = args.output1
out2 = args.output2

# open output files
outfile1 = open(out1, 'a')
outfile2 = open(out2, 'a')

shortname = basename(diamond_result)
evalue = re.split('[_.]', shortname)[6] # isolate e-value
amt = shortname.split('_')[0]
bgalac_reads = int(amt) * 25 # calculate number of bgal reads
not_bgalac_reads = 100000 - bgalac_reads # calculate number of reads that are not bgal
print "Total number of reads derived from beta-galactosidase in ", shortname, ": ", bgalac_reads
print "Total number of reads that were not derived from beta-galactosidase in ", shortname, ": ", not_bgalac_reads

# make two lists: one with only bgal IDs, one with all IDs except bgal
test_db_bgalac_ids = []
test_db_no_bgalac_ids = []
with open(test_db, 'rU') as f:
	for line in f:
		if line.startswith('>'):
			# 3 different identifiers for beta galactosidase
			if "eta-galactosidase" in line:
				test_db_bgalac_ids.append(re.split('[> |]', line)[1])
			elif "EABC_CLOPF" in line:
				test_db_bgalac_ids.append(re.split('[> |]', line)[1])
			elif "KSBGL_SPHMU" in line:
				test_db_bgalac_ids.append(re.split('[> |]', line)[1])
			else:
				test_db_no_bgalac_ids.append(re.split('[> |]', line)[1])

print "A check to verify that all beta-galactosidase reads are counted for: ",
print len(test_db_bgalac_ids) # check to verify that all beta-galactosidase reads are counted for

# set counters
TP = 0
FP = 0
diamond_bgal_results = []
with open(diamond_result, 'rU') as f:
	for line in f:
		split_line = re.split('[	|]', line)
		test_db_id = split_line[0] # save id
		diamond_bgal_results.append(test_db_id) # to use later
		# True positive results are beta gal ids that are correctly mapped
		# 	to beta gal (in beta gal diamond results and are beta gal)
		if test_db_id in test_db_bgalac_ids:
			TP += 1
		# False positive results are ids that are incorrectly mapped to
		# 	beta gal (in beta gal diamond results, but not actually beta gal)
		else:
			#print test_db_id
			FP += 1
		bgalac_db_id = split_line[3]
print "True positve result: ", TP
print "False positve result: ", FP

# Find true negative results: any id that is not beta gal and is not mapped
# 	to beta gal (not in the beta gal diamond results)
TN = 0
for id in test_db_no_bgalac_ids:
        if id not in diamond_bgal_results:
                TN += 1

# Find false negative results: any id that is beta gal and is not mapped
# 	to beta gal (not in the beta gal diamond results)
FN = 0
for id in test_db_bgalac_ids:
        if id not in diamond_bgal_results:
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

# TP_rate = float(TP) / bgalac_reads
# FP_rate = float(FP) / not_bgalac_reads

print >> outfile1, evalue,"\t",sensitivity,"\t",specificity,"\t",accuracy
print >> outfile2, evalue,"\t",TP,"\t",FP,"\t",TN,"\t",FN

outfile1.close()
outfile2.close()
