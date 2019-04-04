#!/bin/bash
#SBATCH -t 3:00:00
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu 5000
#SBATCH --mail-user=mltreiber@ucdavis.edu
#SBATCH --mail-type=END

##########################################################################
# Copyright (C) 2017-2018 Michelle Treiber, Danielle Lemay, and Sam Westreich
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
# master_beta.galac.db_analysis_stoolmg.sh
# December 2017 Michelle Treiber and Danielle Lemay, leveraging Sam Westreich's SAMSA2.0
# Michelle Treiber, mltreiber@ucdavis.edu, github.com/mltreiber
#
# This program sets up Beta-galactosidase analysis of 30 large stool metagenomes
#
# The steps are:
#       1. Human read removal with Bmtagger
#       2. Merging with PEAR
#       3. Read cleaning with Trimmomatic
#       4. Annotation using DIAMOND against the Beta-galactosidase database
#       5. Aggregating DIAMOND results into a readable format
#
##########################################################################
#
# VARIABLES - set these paths for each step.
#
#       0. Starting files location
starting_files_location=/path/to/stool_metagenomes/input_files/thirty_large_mg

#       1. Human Read Removal
bmtagger_location=/path/to/bmtools/bmtagger
bbmap_location=/path/to/Programs/BBMap/sh
human_db=/path/to/databases/human_db

#       2. PEAR
pear_location=/path/to/Programs/pear-0.9.6/pear-0.9.6

#       3. Trimmomatic
trimmomatic_location=/path/to/Programs/Trimmomatic-0.33/trimmomatic-0.33.jar

#       4. DIAMOND 
b_galac_database="/path/to/protein_dbs/db_with_B-galac.dmnd"
diamond_location="/path/to/Programs"

#       5. Aggregation
programs=/path/to/stool_metagenomes/Code
B_galac_db="/path/to/golden_databases/protein_dbs/db_with_B-galac.faa"

####################################################################
#
# STEP 1: REMOVING HUMAN READS USING BMTAGGER
# Note: paired-end files are usually named using R1 and R2 in the name.
# Note: if using single-end reads, only need to specify one input flag (-1)

PATH=$PATH:/path/to/programs/bmtools/bmtagger
PATH=$PATH:/path/to/programs/srprism/gnuac/app
module load blast
module load java bbmap
echo "NOW STARTING master_beta.galac.db_analysis_stoolmg.sh AT: "; date
echo "NOW STARTING HUMAN READ REMOVAL STEP AT: "; date

for file in $starting_files_location/SRR5128401_pass_1.fastq
do
        file1=$file
        file2=$(echo $file1 | sed 's/pass_1/pass_2/')
		filename=$(basename "$file1")
        basename=$(echo $filename | cut -f 1 -d "_")
		outname="$starting_files_location/$basename"

        $bmtagger_location/bmtagger.sh -b $human_db/GCA_000001405.26_GRCh38.p11_genomic.bitmask -x $human_db/GCA_000001405.26_GRCh38.p11_genomic.srprism -q 1 -1 $file1 -2 $file2 -o $outname.human.txt
        filterbyname.sh in=$file1 in2=$file2 out=$outname.R1_nohuman.fastq out2=$outname.R2_nohuman.fastq names=$outname.human.txt include=f
done

mkdir $starting_files_location/step_1_BMTagger_output/
mv $starting_files_location/SRR5128401*human* $starting_files_location/step_1_BMTagger_output/

echo "STEP 1 DONE AT: "; date

####################################################################
#
# STEP 2: MERGING OF PAIRED-END FILES USING PEAR
# Note: paired-end files are usually named using R1 and R2 in the name.
# Note: if using single-end sequencing, skip this step (comment out).

cd $starting_files_location/step_1_BMTagger_output

echo "NOW STARTING PAIRED-END MERGING WITH PEAR AT: "; date

for file in $starting_files_location/step_1_BMTagger_output/SRR5128401.R1_nohuman.fastq
do
        file1=$file
        file2=`echo $file1 | awk -F"R1" '{print $1 "R2" $2}'`
        outpath=`echo $file | awk -F"R1" '{print $1 "merged"}'`
        outname=`echo ${outpath##*/}`

        $pear_location -f $file1 -r $file2 -o $outname
done

mkdir $starting_files_location/step_2_PEAR_output/
mv $starting_files_location/step_1_BMTagger_output/SRR5128401*merged* $starting_files_location/step_2_PEAR_output/

echo "STEP 2 DONE AT: "; date

####################################################################
#
# STEP 3: CLEANING FILES WITH TRIMMOMATIC
# Note: if skipping FLASH, make sure that all starting files are in the
#$starting_files_location/step_2_PEAR_output/ folder!

echo "NOW STARTING READ CLEANING WITH TRIMMOMATIC AT: "; date

module load java
for file in $starting_files_location/step_2_PEAR_output/SRR5128401*merged.assembled.fastq
do
        shortname=`echo $file | awk -F"assembled.fastq" '{print $1 "cleaned.fastq"}'`
        java -jar $trimmomatic_location SE -phred33 $file $shortname SLIDINGWINDOW:4:15 MINLEN:99
done

mkdir $starting_files_location/step_3_trimmomatic_output/
mv $starting_files_location/step_2_PEAR_output/SRR5128401*cleaned.fastq $starting_files_location/step_3_trimmomatic_output/

echo "STEP 3 DONE AT: "; date

####################################################################
# STEP 4: ANNOTATING WITH DIAMOND AGAINST BETA-GALACTOSIDASE
# Note: this step assumes that the DIAMOND database is already built.  If not,
# do that first before running this step.

cd $starting_files_location
echo "NOW STARTING DIAMOND BETA-GALACTOSIDASE ANNOTATIONS AT: "; date

for file in $starting_files_location/step_3_trimmomatic_output/merged_results/SRR5128401*cleaned.fastq
do
         shortname=`echo $file | awk -F"cleaned.fastq" '{print $1 "annot_BGALAC"}'`
         echo "Now starting on " $file
		 echo $shortname.txt

         $diamond_location/diamond blastx --db $b_galac_database -q $file -a $file.bgalac.dmd -t ./ -k 1 --sensitive --evalue 1e-10
         $diamond_location/diamond view --daa $file.bgalac.dmd.daa -o $shortname.txt -f tab
done

mkdir -p $starting_files_location/step_4_DIAMOND_output/beta_gal/merged_results/
mkdir $starting_files_location/step_4_DIAMOND_output/binary_output/
mv $starting_files_location/step_3_trimmomatic_output/merged_results/SRR5128401*annot_BGALAC* $starting_files_location/step_4_DIAMOND_output/beta_gal/merged_results/
mv $starting_files_location/step_3_trimmomatic_output/*.daa $starting_files_location/step_4_DIAMOND_output/binary_output/

echo "DIAMOND ANNOTATIONS AGAINST BETA-GALACTOSIDASE DATABASE DONE AT: "; date

####################################################################
#
# STEP 5: PYTHON BETA-GALACTOSIDASE ANALYSIS COUNTER

echo "NOW STARTING AGGREGATION OF DIAMOND BETA-GALACTOSIDASE RESULTS AT: "; 	date

# Create Beta-galactosidase text with all family names:

bash $programs/b-galac-counts.sh > $starting_files_location/step_4_DIAMOND_output/stool_mg_bgalac_counts.table.txt

mkdir $starting_files_location/step_5_aggregation_output/
mv $starting_files_location/step_4_DIAMOND_output/*table* $starting_files_location/step_5_aggregation_output/

echo "BETA-GALACTOSIDASE AGGREGATION STEP DONE AT: "; date

####################################################################
