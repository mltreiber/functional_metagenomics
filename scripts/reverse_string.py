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
# reverse_string.py
# Created January 30, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to take the reverse complement of each sequence
# within a metagenome and print to an output file. 
#
##########################################################################
#
# Example input file in fastq format:
# @SRR5128401.1.2 HWI-ST1276:191:C4HV5ACXX:4:1101:1408:1984 length=100
# TACAGATACAATGTTTTCCACTTGCTCTTCACCCCCTTTTTCCCCTTTTTCTCCTTTTTGTATTGTTCCTTGTGTTTGGTCATTACTCCCTGGTCCACAT
# +
# ?@1:;D+B4C?DF4CFF:A?EDI+<CBCBBF+9?D1??BFCB?3)0)0*0?<?*0?F>F#########################################
# @SRR5128401.2.2 HWI-ST1276:191:C4HV5ACXX:4:1101:1633:1987 length=100
# CAGATTCCATTTTTCTCTTCACATCGTTGAGCTTTGCTACCCAACTTCCTCACTTCACATTGGAGAAGAGCTTCCCGTGGTTGTGATGGGGACTTTAATG
# +
# ?:B+4A22=DDFFE:A<EICJID>@H:+A3AG@1??1?9:C8*)00:0??0989E?F?9*..=3=)(8@G)=D4775.5<B7?#################
#
# Example output file in fastq format:
# @SRR5128401.1.2 HWI-ST1276:191:C4HV5ACXX:4:1101:1408:1984 length=100
# ATGTGGACCAGGGAGTAATGACCAAACACAAGGAACAATACAAAAAGGAGAAAAAGGGGAAAAAGGGGGTGAAGAGCAAGTGGAAAACATTGTATCTGTA
# +
# ?@1:;D+B4C?DF4CFF:A?EDI+<CBCBBF+9?D1??BFCB?3)0)0*0?<?*0?F>F#########################################
# @SRR5128401.2.2 HWI-ST1276:191:C4HV5ACXX:4:1101:1633:1987 length=100
# CATTAAAGTCCCCATCACAACCACGGGAAGCTCTTCTCCAATGTGAAGTGAGGAAGTTGGGTAGCAAAGCTCAACGATGTGAAGAGAAAAATGGAATCTG
# +
# ?:B+4A22=DDFFE:A<EICJID>@H:+A3AG@1??1?9:C8*)00:0??0989E?F?9*..=3=)(8@G)=D4775.5<B7?#################
#
##########################################################################
from Bio.Seq import Seq

input = "/path/to/stool_metagenomes/input_files/thirty_large_mg/step_1_BMTagger_output/SRR5128401.R2_nohuman.fastq"
output = "/path/to/stool_metagenomes/input_files/thirty_large_mg/step_1_BMTagger_output/SRR5128401.R2_nohuman_reverse_complement.fastq"

out = open(output, "w")

counter = 1
with open(input, "rU") as f:
	for line in f:
#		print counter
		if counter == 2:
			line = line.rstrip()
#			print "FOUND SEQUENCE"
#			print line
			line = Seq(line)
			line = line.reverse_complement() + "\n"
#			print "REVERSE COMPLEMENT OF SEQUENCE"
#			print line
		print >> out, line,
		counter += 1
		if counter > 4:
			counter = 1
