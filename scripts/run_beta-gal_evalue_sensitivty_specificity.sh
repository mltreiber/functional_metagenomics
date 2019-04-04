#!/usr/bin/bash

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
# run_beta-gal_evalue_sensitivty_specificity.sh
# Created January 2, 2018
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Bash script created to run sensitivty_specificity_beta_gal_evalue.py
# as a loop over multiple files creating two final output tables with
# results for multiple DIAMOND output files varying in e-value parameters
#
##########################################################################

starting_location=/path/to/bgalac_simulated_mg/100ave_reads
#mkdir $starting_location/step_3_TP_and_FP_rates_output/test_evalue
output1="$starting_location/step_3_TP_and_FP_rates_output/test_evalue/100rl_sensitivty_specificity_bgal_evalue_extended.txt"
output2="$starting_location/step_3_TP_and_FP_rates_output/test_evalue/100rl_TP_FP_TN_FN_bgal_evalue_extended.txt"
test_db="$starting_location/100_test_database.mg.fna"

# Make headers for both output tables
echo -e "E-value\tsensitivity\tspecificity\taccuracy" > $output1
echo -e "E-value\tTP\tFP\tTN\tFN" > $output2

for diamond_result in $starting_location/step_1_DIAMOND_output/test_evalue/100_test_database.mg.annot_BGALAC_1e-{3..100}.txt
do
	echo $diamond_result
	python sensitivty_specificity_beta_gal_evalue.py -db $test_db -i $diamond_result -o1 $output1 -o2 $output2
done
exit
