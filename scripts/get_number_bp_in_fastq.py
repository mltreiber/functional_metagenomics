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
# get_number_bp_in_fastq.py
# Created June, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Python script created to get the average read length of each metagenome
# from the merged reads output files
#
##########################################################################
import os

input_path="/path/to/stool_metagenomes/input_files/thirty_large_mg/step_2_PEAR_output"

overall_count_list = []
for filename in os.listdir(input_path):         # loop through files in specified directory
    if filename.endswith(".merged.assembled.fastq"):
        print filename
        with open(os.path.join(input_path, filename), 'rU') as f:
                counter = 1
                current_count_list = []
                for line in f:
                        if counter == 2:
                                line = line.strip()
                                overall_count_list.append(len(line))
                                current_count_list.append(len(line))
                                counter += 1
                        elif counter == 4:
                                counter = 1
                        else:
                                counter += 1
#               print current_count_list
                print sum(current_count_list) / float(len(current_count_list))
print "OVERALL READ LENGTH AVERAGE"
#print overall_count_list
print sum(overall_count_list) / float(len(overall_count_list))
