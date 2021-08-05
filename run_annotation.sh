######################
### VCF Annotation ###
######################
# Before you run this program:
# - Make sure you have the sequence_ontology.csv in the same folder. Jump to the second section to find how to download it.
# - Make sure python and its packages (such as pandas) are installed.

# Uncomment the following code to perform the annotation on default input file (Challenge_data_(1).vcf) 
# and save the output to the default file (output.tsv):

# python download_sequence_ontology.py

# Alternatively, you can also modify the input file and/or the output path, for example:
python vcf_annotation.py --input_path test_input.vcf --output_path test_output.tsv




###############################################
### Downloading the Sequence Ontology Table ###
###############################################
# - Make sure there is a chromedriver app in the same folder. If not, please download it from its official website.
# - Make sure python and its packages (such as selenium, pandas) are installed.

# Uncomment the following code to download the Sequence Ontology Table:

# python download_sequence_ontology.py 
