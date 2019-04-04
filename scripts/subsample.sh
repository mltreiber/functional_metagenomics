# !/usr/bin/bash

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
# subsample.sh
# Created August, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Bash script created to subsample a large metagenome into multiple
# smaller metagenomes and printing subsamples to an output file.
#
##########################################################################

starting_location="/share/lemaylab-backedup/milklab/michelle/functional_db_comparison/stool_metagenomes/read_depth_test/SRR5127734"
output_location="/share/lemaylab-backedup/milklab/michelle/functional_db_comparison/stool_metagenomes/read_depth_test/SRR5127734/raw_subsamples"
file="$starting_location/SRR5127734.R1_headers.txt"
shortname="SRR5127734_"

counter=1
while [ $counter -le 10 ]
do
	echo "100k_"$shortname$counter
	shuf -n 100000 $file  > "$output_location/100k_"$shortname$counter".txt"
	echo "200k_"$shortname$counter
	shuf -n 200000 $file  > "$output_location/200k_"$shortname$counter".txt"
        echo "300k_"$shortname$counter
        shuf -n 300000 $file  > "$output_location/300k_"$shortname$counter".txt"
        echo "400k_"$shortname$counter
        shuf -n 400000 $file  > "$output_location/400k_"$shortname$counter".txt"
        echo "500k_"$shortname$counter
        shuf -n 500000 $file  > "$output_location/500k_"$shortname$counter".txt"
        echo "1mil_"$shortname$counter
        shuf -n 1000000 $file  > "$output_location/1mil_"$shortname$counter".txt"
        echo "2mil_"$shortname$counter
        shuf -n 2000000 $file  > "$output_location/2mil_"$shortname$counter".txt"
	#echo "3mil_"$shortname$counter
        #shuf -n 3000000 $file  > "$output_location/3mil_"$shortname$counter".txt"
	#echo "4.5mil_"$shortname$counter
        #shuf -n 4500000 $file  > "$output_location/4.5mil_"$shortname$counter".txt"
        echo "5mil_"$shortname$counter
        shuf -n 5000000 $file  > "$output_location/5mil_"$shortname$counter".txt"
        echo "10mil_"$shortname$counter
        shuf -n 10000000 $file  > "$output_location/10mil_"$shortname$counter".txt"
        echo "20mil_"$shortname$counter
        shuf -n 20000000 $file  > "$output_location/20mil_"$shortname$counter".txt"
	((counter++))
done
