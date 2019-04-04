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
# sort_golden_db.py 
# Created August 30, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to sort golden database into two sub-databases:
# One that contains the enzyme of interest and the other that contains
# all other proteins that are not the enzyme of interest.
#
##########################################################################
#
# Usage:
#
# -db 		 database 		 	Fasta-formatted golden database with known
#									amount of enzyme of interest
#
# -out1 	output file 1		The output file name that contains the 
#									sub-database with the enzyme of 
#									interest
#
# -out2 	output file 2 		The output file name that contains the 
# 									sub-database with all other proteins
#
# Example usage: python sort_golden_db.py -db golden_db.fasta -out1 db_with_B-galac.fasta -out2 db_without_B-galac.fasta
#
##########################################################################

from sys import argv
from Bio import SeqIO
import argparse

# Create flag arguments:
parser = argparse.ArgumentParser()

parser.add_argument("-db", "--database", dest = "db", help = "golden database") 							# First flag argument
parser.add_argument("-out1", "--output1", dest = "out1", help = "output file with enzyme of interest")		# Second flag argument
parser.add_argument("-out2", "--output2", dest = "out2", help = "output file without enzyme of interest")	# Third flag argument

args = parser.parse_args()

# Check if enough arguments have been passed
if len(vars(args)) != 3:
	print 'ERROR: Too few arguments. Must include a database, name of output file with enzyme of interest, and name of output file without enzyme of interest'
	print 'Example usage: python sort_golden_db.py -db golden_db.fasta -out1 db_with_B-galac.fasta -out2 db_without_B-galac.fasta'

print 'Database: ' + args.db
print 'Output file one containing enzyme of interest: ' + args.out1
print 'Output file two without enzyme of interest: ' + args.out2

fasta_db = args.db
output1 = args.out1
output2 = args.out2

# open output files to write to
out1 = open(output1, 'w')
out2 = open(output2, 'w')

with open(fasta_db, 'rU') as f:
	for record in SeqIO.parse(fasta_db, 'fasta'):						# read as a fasta file
		header = record.description 									# save single line description
		lowercase_header = header.lower()								# make description all lowercase
		if 'beta-galactosidase' in lowercase_header: 					# match item with case insensitivity
			print >> out1, record.format("fasta"),						# print full header and sequence to output 1 if there is a match
		else:
			print >> out2, record.format("fasta"),						# print full header and sequence to output 2 if there is not a match
