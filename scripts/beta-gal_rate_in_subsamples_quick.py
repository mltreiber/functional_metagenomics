#!/bin/python

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
# beta-gal_rate_in_subsamples_quick.py
# Created January 30, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to count the abundance of beta-gal 
# in all subsamples of large stool metagenome. This script is 
# made to run as a loop using run_beta-gal_rate_in_subsamples_quick.sh.
#
# Note: must change pathway on line 101 to use.
#
##########################################################################
#
# Usage:
#
# -in1		input file 1		Trimmed metagenome subsample created from
#									large stool metagenome
#
# -in2		input file 2		DIAMOND output of fully trimmed metagenome
#									containing all metagenomes annotated 
#									to 
#
# -out		output filename		The beta-gal percent and total count in
#									the subsample
#
# Example usage: python beta-gal_rate_in_subsamples.py -in1 100k_SRR5127734_1.txt -in2 SRR5127734.annot_BGALAC.txt -out SRR5127734_merged_subsamples_beta-gal_rates.txt
#
##########################################################################
#
# Example input file 1:
# @SRR5127721.4059634.1 4059634 length=90
# @SRR5127721.14536737.1 14536737 length=101
# @SRR5127721.9100819.1 9100819 length=101
# @SRR5127721.13243526.1 13243526 length=101
# @SRR5127721.13434367.1 13434367 length=101
#
# Example input file 2:
# SRR5127721.2203.1       2514067395      100.0   38      0       0       2       115     538     575     5.5e-21 87.0
# SRR5127721.3038.1       2514067395      49.2    59      30      0       179     3       493     551     4.8e-16 71.2
# SRR5127721.3176.1       sp|A1A399|BGAL_BIFAA    97.8    45      1       0       137     3       306     350     1.8e-23 95.5
# SRR5127721.5134.1       sp|Q9KI47|BGAL_PLASS    78.4    51      11      0       154     2       308     358     1.8e-19 82.4
#
# Example of output file:
# 100k_SRR5127721_1 33 0.033
# 100k_SRR5127721_2 38 0.038
# 100k_SRR5127721_3 29 0.029
# 100k_SRR5127721_4 29 0.029
# 100k_SRR5127721_5 33 0.033
#
##########################################################################

from sys import argv
from os.path import basename
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-in1", "--input1", dest = "in1", help = "subsample of trimmed metagenome") 	 # First flag argument
parser.add_argument("-in2", "--input2", dest = "in2", help = "DIAMOND output of full trimmed metagenome")	 # Second flag argument
parser.add_argument("-out", "--output", dest = "out", help = "the beta-gal percent and total count")		 # Third flag argument

args = parser.parse_args()
store = vars(args)
count = sum([ 1 for a in store.values( ) if a]) # total number of arguments passed through the command line

# Check if enough arguments have been passed
if count != 3:
	print 'ERROR: Must include two input files and an output file name for the beta-gal rate output'
	print 'Example usage: python beta-gal_rate_in_subsamples.py -in1 100k_SRR5127734_1.txt -in2 SRR5127734.annot_BGALAC.txt -out SRR5127734_merged_subsamples_beta-gal_rates.txt'
	sys.exit()

# Save arguments to variables
file = args.in1
diamond = args.in2
rate_output = args.out

# Save file identity
basename = basename(file)
print "Now annotating: ", basename
name_no_ext = basename.rsplit('.', 1)[0]
sample_id = name_no_ext.split('_')[1]
output = "/path/to/stool_metagenomes/read_depth_test/" + sample_id + "/step_4_DIAMOND_output/all_subsamples/" + name_no_ext + ".merged_annot_BGALAC.txt"

# Save/open output files
out = open(output, 'w')
rate_out = open(rate_output, 'a')

# save all IDs from subsample and total number of reads
line_count = 0
subsample_ids = []
with open(file, 'rU') as f:
	for line in f:
		line_count += 1
		ID = re.split('[@ ]', line)[1]
		subsample_ids.append(ID)
print "Total number of reads in subsample: ", line_count

# Save DIAMOND annotation output from whole metagenome to a list
diamond_results = []
with open(diamond, 'rU') as f:
	for line in f:
		line = re.split('\s', line)[0]
		diamond_results.append(line)

# Find all subsample IDs that mapped to beta-gal using DIAMOND
# annotation output from whole metagenome by finding matches between 
# two lists:
matches = set(subsample_ids).intersection(diamond_results)

# calculate percent beta-gal in subsample and print to output file
counter = 0
for i in matches:
	counter += 1
	print >> out, i
print "Total number of beta-gal in subsample is: ", counter

rate = float(counter) / float(line_count)
percent_bgal = rate * 100
print "Percent of beta-gal is: ", percent_bgal
print >> rate_out, name_no_ext, counter, percent_bgal
