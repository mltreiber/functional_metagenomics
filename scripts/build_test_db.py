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
# build_test_db.py
# Created August 30, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to build 100 test databases with an increasing
# amount of enzyme of interest (1/5,000 to 100/5,0000)
#
# Note: must change pathway on line 101 to use.
#
##########################################################################
#
# Usage:
#
# -db1		database 1		Fasta formatted database that contains sequences 
#								from only the enzyme of interest
#
# -db2		database 2		Fasta formatted database that contains sequences
#								from all other proteins that are not the enzyme
#								of interest
#
# Example usage: python build_test_db.py -db1 db_with_B-galac.fasta -db2 db_without_B-galac.fasta
#
###########################################################################

from sys import argv
from Bio import SeqIO
from random import sample
import argparse
import numpy as np 

# Create flag arguments:
parser = argparse.ArgumentParser()

parser.add_argument("-db1", "--database1", dest = "db1", help = "database with enzyme of interest") 	 # First flag argument
parser.add_argument("-db2", "--database2", dest = "db2", help = "database without enzymre of interest")	 # Second flag argument

args = parser.parse_args()

# Check if enough arguments have been passed
if len(vars(args)) != 2:
	print 'ERROR: Too few arguments. Must include two input files: one containing enzyme of interest, and one without enzyme of interest interest'
	print 'Example usage: python build_test_db.py -db1 db_with_B-galac.fasta -db2 db_without_B-galac.fasta'
	sys.exit() 

print 'Database 1: ' + args.db1
print 'Database 2: ' + args.db2

enz_db = args.db1
no_enz_db = args.db2

total = 4000	# Set total number sequences in each test database 

for i in range(1,101):								# Range determines how many test databases to create		
	remainder = total - i 							# Number of sequences from db without enzyme of interest
	outname = '%s_test_database.fa' % (i)			# Out file name	
	out = open(outname, 'w')
	print 'Creating: ', outname

	with open(enz_db, 'rU') as f:
		enz_seqs = SeqIO.parse(f, 'fasta')
		for record in np.random.choice(list(enz_seqs), i, replace=True):	# Randomly choose i number of records from enz_db
			print >> out, record.format("fasta"),	# Print to output: i number of sequences
	
	with open(no_enz_db, 'rU') as f:
		no_enz_seqs = SeqIO.parse(f, 'fasta')			
		for record in sample(list(no_enz_seqs), remainder): # Randomly choose remainder number of records from no_enz_db
			print >> out, record.format("fasta"),   		# Print to output: remainder number of sequences
	
	out.close()
	i = i + 1
