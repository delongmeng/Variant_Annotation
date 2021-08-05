'''
This program aims to annotate an input Variant Call Formal (VCF) file with the following information:
- Type of variation (substitution, insertion, CNV, etc.) and their effect (missense, silent, intergenic, etc.). If there are multiple effects, 
	annotate with the most deleterious possibility.
- Depth of sequence coverage at the site of variation.
- Number of reads supporting the variant.
- Percentage of reads supporting the variant versus those supporting reference reads.
- Allele frequency of variant from ExAC API (API documentation is available here: http://exac.hms.harvard.edu/).

Note that this program is hardcoded to process input files with two samples called "normal" and "vaf5". It needs to be modified to process documents
with other sample names.
This program rely on a sequence ontology file to provide information of servereness of variation consequences. 
Make sure you have the sequence_ontology.csv in the same folder. If not, run the download_sequence_ontology.py program to download it.

To run this program, make sure packages (such as pandas) are installed, and then simply type the following code in command line:
python vcf_annotation.py
Also, default input file (Challenge_data_(1).vcf) and output path (output.tsv) can be modified, for example:
python vcf_annotation.py --input_path test_input.vcf --output_path test_output.tsv
'''

import pandas as pd
import argparse
from utilities import *

def main():

	# take arguments from the command (the input path and output path)
	in_arg = get_input_args()

	# import the sequence ontology (so) table with score (rank, the lower the score the more severe the variant consequence is) 
	# store the relationship between the so and score using so_to_score or score_to_so mappings
	# will use this to determine which consequence is the most deleterious for a given variant 
	so = pd.read_csv('sequence_ontology.csv')
	so = so.rename(columns = {"Unnamed: 0": "score", "SO term": "so_term"})
	so_to_score = dict(zip(so["so_term"], so["score"]))
	score_to_so = dict(zip(so["score"], so["so_term"]))

    # according to the challenge requirement, we'll add these columns to the output file
	variables_to_add = ["type_variation", "variation_effect", "depth_coverage_normal", "depth_coverage_vaf5", \
		"n_reads_var_normal", "n_reads_var_vaf5", "perc_var_normal", "perc_ref_normal","perc_var_vaf5", "perc_ref_vaf5", "allele_freq"]

    # annotate the input data and save the result to the output file
	annotate(in_arg.input_path, in_arg.output_path, variables_to_add, so_to_score, score_to_so)

# Call the main function to run the program
if __name__ == "__main__":
	main()

