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
# old_NCBI_format.py
# Created October 7, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to format fasta headers into the old NCBI format
#
##########################################################################
#
# Usage:
#
# -I		input file		Fasta formatted database
#
# -O		output file		Fasta formatted database with headers 
#								in old NCBI format
#
# Example usage: python old_NCBI_format.py -I unique_golden_db.fna -O uniq_gold_db_NCBIformat.fna
#
##########################################################################
#
# Example input header:
# >4HBCL_RHOPA Q53005 4-hydroxybenzoate--CoA/benzoate--CoA ligase OS=Rhodopseudomonas palustris (strain ATCC BAA-98 / CGA009) GN=hbaA PE=1 SV=1
#
# Example output header:
# >gi|-1|ref|XYZ|4HBCL_RHOPA Q53005 4-hydroxybenzoate--CoA/benzoate--CoA ligase OS=Rhodopseudomonas palustris (strain ATCC BAA-98 / CGA009) GN=hbaA PE=1 SV=1 linear
# 
##########################################################################

import sys
from sys import argv
import argparse
from Bio import SeqIO

# Create flag arguments:
parser = argparse.ArgumentParser()

parser.add_argument("-I", "--in", dest = "input", help = "fasta formatted nucleotide database") 	 # First flag argument
parser.add_argument("-O", "--out", dest = "output", help = "fasta formatted database with headers in old NCBI format")	 # Second flag argument

args = parser.parse_args()

# Check if enough arguments have been passed
if len(vars(args)) != 2:
	print 'ERROR: Too few arguments. Must include a fasta formatted input file and a specified output file'
	print 'Example usage:  python old_NCBI_format.py -I unique_golden_db.fna -O uniq_gold_db_NCBIformat.fna'
	sys.exit()

print 'Input file: ' + args.input
print 'Output file: ' + args.output

# Set variables:
fasta_file = args.input
out_file = args.output

out = open(out_file, 'w')

with open(fasta_file, 'rU') as f:
	for line in f:
		if line.startswith('>'):
			line = line.rstrip('\n')
			# print old NCBI formatted header to output file by addition of 'gi|-1|ref|XYZ|' and ' linear'
			print >> out, line[:1] + 'gi|-1|ref|XYZ|' + line[1:] + ' linear'
		else:
			print >> out, line,
		
out.close()
