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
# find_R1_and_R2_matches_4.25.18.py 
# Created July 25, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to find number of all Query Seq IDs from R1 and 
# R2 reads that match: same Query Seq ID mapping to the same Subject Seq ID. 
# The congruent matches are printed to an output file:
#	Query Seq ID 	Subject Seq ID
# 
#
##########################################################################

starting_location = "/path/to/stool_metagenomes/input_files/thirty_large_mg/step_4_DIAMOND_output/beta_gal/"
R1_in = starting_location + "R1_read_results/SRR5128401.R1_annot_BGALAC.txt"
R2_in = starting_location + "R2_read_results/SRR5128401.R2_annot_BGALAC_reverse_complement.txt"
output = starting_location + "SRR5128401.congruent_annot_BGALAC.txt"

# Create dictionary from R1 Results
# Query Seq ID : Subject Seq ID
# Example - 'K00188:230:HG35HBBXX:6:1101:19502:21606': ''
R1_dictionary = {}
with open(R1_in, "r") as f:
        for line in f:
                line = line.split()
		query = line[0][:-2] # remove R1 specification
                R1_dictionary[query] = line[1]

# Create dictionary from R2 Results
# Query Seq ID : Subject Seq ID
# Example - 'K00188:230:HG35HBBXX:6:1101:19502:21606': ''
R2_dictionary = {}
with open(R2_in, "r") as f:
        for line in f:
                line = line.split()
		query = line[0][:-2] # remove R2 specification
                R2_dictionary[query] = line[1]

# Make dictionaries into seets for quick analysis
R1_set = set(R1_dictionary)
R2_set = set(R2_dictionary)

# Find number of matching Query Seq IDs
print "Number of Query Seq IDs in both R1 and R2: ", len(R1_set.intersection(R2_set))

# Find number of Query Seq IDs in R1 that are not in R2
unique_R1_mg_ids = 0
for k in R1_dictionary.keys():
	if k not in R2_dictionary.keys():
		unique_R1_mg_ids += 1
#		print "Unique R1 Query Seq IDs", k
	else:
		continue
		#print "MATCHING IDs: ", k,

print "Number of Query Seq IDs in R1 that are not in R2: ", unique_R1_mg_ids

# Find number of Query Seq IDs in R2 that are not in R1
unique_R2_mg_ids = 0
for k in R2_dictionary.keys():
	if k not in R1_dictionary.keys():
		unique_R2_mg_ids += 1
	else:
		continue
print "Number of Query Seq IDs in R2 that are not in R1: ", unique_R2_mg_ids

# open output file
out = open(output, 'w')

# Find number of matching Query Seq IDs that also map to the same Subject Seq ID
matching_query_subject_ids = 0
for id in R1_set.intersection(R2_set):
	if R1_dictionary[id] == R2_dictionary[id]:
		# Print the matching Query Seq IDs that also map to the same Subject Seq ID to output file
		print >> out, "%s\t%s" % (id, R1_dictionary[id])
		matching_query_subject_ids += 1
	else:
		continue
	# 	print "NON-MATCHING: ", id

print "Number of matching Query Seq IDs that also map to the same Subject Seq ID: ", matching_query_subject_ids
