Recommendations for functional metagenomics of fecal microbiomes


master_beta.galac.db_analysis_stoolmg.sh: This program was designed to set up the Beta-galactosidase analysis of 30 large stool metagenomes using the following steps:
      1. Human read removal with Bmtagger
      2. Merging with PEAR
      3. Read cleaning with Trimmomatic
      4. Annotation using DIAMOND against the Beta-galactosidase database
      5. Aggregating DIAMOND results into a readable format

Human Read Removal with BMTagger:
      For this step, the user must download the following modules: blast, bbmap, and bmtagger.

Merging with Pear:
      For this step, the user must download pear version 0.9.6.
      
Read cleaning with Trimmomatic:
      For this step, the user must download trimmomatic version 0.33
     
Annotation step using DIAMOND:
      For this step, user must download DIAMOND dependencies
      
Aggregation step:
      For this step, user can use b-galac-counts.sh


b-galac-counts.sh: Bash script created to give total counts of beta-galactosidase matches
for each DIAMOND annotation output that have increasing doses of
beta-galactosidase

beta-gal_rate_in_subsamples_quick.py: Python script created to count the abundance of beta-gal 
in all subsamples of large stool metagenome. This script is 
made to run as a loop using run_beta-gal_rate_in_subsamples_quick.sh.

build_test_db.py: Python script created to build 100 test databases with an increasing
amount of enzyme of interest (1/5,000 to 100/5,0000)

find_R1_and_R2_matches_4.25.18.py: Python script created to find number of all Query Seq IDs from R1 and 
R2 reads that match: same Query Seq ID mapping to the same Subject Seq ID. 
The congruent matches are printed to an output file:
Query Seq ID 	Subject Seq ID

get_number_bp_in_fastq.py: Python script created to get the average read length of each metagenome
from the merged reads output files

get_number_reads.sh: Python script created to count total number of reads in a metagenome

old_NCBI_format.py: Python script created to format fasta headers into the old NCBI format

reverse_string.py: Python script created to take the reverse complement of each sequence
within a metagenome and print to an output file.

run_HTA_evalue_sensitivty_specificity.sh: Bash script created to run sensitivty_specificity_HTA_evalue.py
as a loop over multiple files creating two final output tables with
results for multiple DIAMOND output files varying in e-value parameters

run_beta-gal_evalue_sensitivty_specificity.sh: Bash script created to run sensitivty_specificity_beta_gal_evalue.py
as a loop over multiple files creating two final output tables with
results for multiple DIAMOND output files varying in e-value parameters

run_beta-gal_rate_in_subsamples.sh: Bash script created to count the abundance of beta-gal 
in all subsamples of large stool metagenome. This script is 
made to run beta-gal_rate_in_subsamples_quick.sh.

sensitivty_specificity_HTA_evalue.py: Python script created to calculate true positive, false positive, true
negative, and false negative rates and print to a table in preparation for an ROC curve.
Script will also calculate specificity, sensitivity, and accuracy
and create another output table for those results.

sensitivty_specificity_beta_gal_evalue.py: Python script created to calculate true positive, false positive, true
negative, and false negative rates and print to a table in preparation for an ROC curve.
Script will also calculate specificity, sensitivity, and accuracy
and create another output table for those results.

sort_golden_db.py: Python script created to sort golden database into two sub-databases:
One that contains the enzyme of interest and the other that contains
all other proteins that are not the enzyme of interest.

subsample.sh: Bash script created to subsample a large metagenome into multiple
smaller metagenomes and printing subsamples to an output file.
