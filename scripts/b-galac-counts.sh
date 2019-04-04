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
# b-galac-counts.sh
# Created October, 2017
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# Bash script created to give total counts of beta-galactosidase matches
# for each DIAMOND annotation output that have increasing doses of
# beta-galactosidase
#
##########################################################################

file_path=/path/to/stool_metagenomes/input_files
for file in $file_path/step_4_DIAMOND_output/*annot_BGALAC.txt
do
	shortname=${file##*/}
	dose=$(echo $shortname | cut -f 1 -d '_')
	count=$(cat $file | wc -l)
	match="$dose, $count"
	echo $match
done
