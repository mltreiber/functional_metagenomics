#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH --cpus-per-task 20
#SBATCH --mem-per-cpu 2000
#SBATCH --mail-user=mltreiber@ucdavis.edu
#SBATCH --mail-type=END

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
# run_beta-gal_rate_in_subsamples.sh
# Created February 2, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Bash script created to count the abundance of beta-gal 
# in all subsamples of large stool metagenome. This script is 
# made to run beta-gal_rate_in_subsamples_quick.sh.
#
##########################################################################


starting_location=/path/to/stool_metagenomes/read_depth_test
code=/path/to/stool_metagenomes/Code/python_scripts
subsample_location=$starting_location/SRR5127721/raw_subsamples
diamond_file="$starting_location/SRR5127721/step_4_DIAMOND_output/SRR5127721.merged.annot_BGALAC.txt"
output_file="$starting_location/SRR5127721/step_5_aggregation_output/merged_results/100k_SRR5127721_merged_beta-gal_rates.txt"

###echo -e "subsample\ttotal_beta-gal\tpercent_beta-gal" >> $output_file

for file in $subsample_location/100k_SRR5127721_{1..10}.txt
do
	python $code/beta-gal_rate_in_subsamples_quick.py -in1 $file -in2 $diamond_file -out $output_file
done
exit
