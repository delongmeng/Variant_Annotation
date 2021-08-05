## Variant Call Format (VCF) Annotation


### The Task

This is a variant annotation tool. Each variant needs to be annotated with the following pieces of information:  

1. Type of variation (substitution, insertion, CNV, etc.) and their effect (missense, silent,
intergenic, etc.). If there are multiple effects, annotate with the most deleterious
possibility.  
2. Depth of sequence coverage at the site of variation.  
3. Number of reads supporting the variant.  
4. Percentage of reads supporting the variant versus those supporting reference reads.  
5. Allele frequency of variant from ExAC API (API documentation is available here:
http://exac.hms.harvard.edu/).  
6. Any additional annotations that you feel might be relevant.  

### The Program

#### Overview

Variant annotation is a critical step of genomic analysis. This program read the input Variant Call Format (VCF) file (`Challenge_data_(1).vcf` here) and add annotations to each row of data. According to the instructions shown above, it keeps original data of the input file the same, and adds 11 extra columns:

| Column Name           | Description                                                                        | Source                                                                                                                          | Note                     |
|-----------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| type_variation        | type of variation (substitution, insertion, CNV, etc.)                             | from "INFO"-"TYPE"                                                                                                              | for each possible allele |
| variation_effect      | variation effect or the most deleterious possibility if there are multiple effects | from the "vep_annotations" of ExAC API, and the most deleterious effect of each allele is determined by the "sequence ontology" | for each possible allele |
| depth_coverage_normal | depth of sequence coverage at the site of variation for the sample "normal"        | from "DP" of given sample                                                                                                       |                          |
| depth_coverage_vaf5   | depth of sequence coverage at the site of variation for the sample "vaf5"          | from "DP" of given sample                                                                                                       |                          |
| n_reads_var_normal    | number of reads supporting the variant for the sample "normal"                     | from "AO" of given sample                                                                                                       | for each possible allele |
| n_reads_var_vaf5      | number of reads supporting the variant for the sample "vaf5"                       | from "AO" of given sample                                                                                                       | for each possible allele |
| perc_var_normal       | percentage of reads supporting the variant for the sample "normal"                 | from "AO" and "DP" of given sample                                                                                              | for each possible allele |
| perc_ref_normal       | percentage of reads supporting the reference for the sample "normal"               | from "RO" and "DP" of given sample                                                                                              |                          |
| perc_var_vaf5         | percentage of reads supporting the variant for the sample "vaf5"                   | from "AO" and "DP" of given sample                                                                                              | for each possible allele |
| perc_ref_vaf5         | percentage of reads supporting the reference for the sample "vaf5"                 | from "RO" and "DP" of given sample                                                                                              |                          |
| allele_freq           | allele frequency of variant                                                        | from ExAC API                                                                                                                   | for each possible allele |


Note that some alleles have multiple effects on the gene they are located at. To determine the "most deleterious" effect of each allele, a rank of the severeness of these effects is needed. I used the standard defined by ["Sequence Ontology"](https://m.ensembl.org/info/genome/variation/prediction/predicted_data.html). I downloaded the Sequence Ontology table using the program `download_sequence_ontology.py`, and saved the table to `sequence_ontology.csv`, which is used by the annotation program `vcf_annotation.py`.

Also note that the annotation program is hardcoded to process input files with two samples called "normal" and "vaf5". It needs to be modified to process documents with other sample names.

#### How to use this program?

**Environment**

- To run the annotation, you will need Python and some common packages (pandas, requests, and argparse).
- To run the sequence ontology downloader, you will need Python and its packages (pandas and requests), as well as the selenium package to set up the web driver. You will also need a chrome driver (already provided here). 

**Shell script**

- You can directly run the `run_annotation.sh` shell script in your command line terminal. Make sure the premission of this file is set to include "execute".
- There are some sample code in the `run_annotation.sh` file. Directly running this file will perform annotation on a small test input file and generate a test output file.
- Please read the instruction in the `run_annotation.sh` file and feel free to modify it as needed. For example, you can perform the annotation on the full `Challenge_data_(1).vcf` file or any other input file. You can also run the sequence ontology downloader.


**Python script**

- You can run the `vcf_annotation.py` program to perform annotation. The following code will by default take the `Challenge_data_(1).vcf` file as input and save the output to `output.tsv`:  
```
python vcf_annotation.py
```
- This program can also take arguments to modify the default input file and/or output path, for example:
```
python vcf_annotation.py --input_path test_input.vcf --output_path test_output.tsv
```
- To run the sequence ontology downloader `download_sequence_ontology.py`:  
```
python download_sequence_ontology.py 
```

#### Files

A summary of all the files in this folder:  
- `Challenge_data_(1).vcf`: the default input VCF data to be annotated  
- `test_input.vcf`: a small test input VCF data to be annotated  
- `output.tsv`: the output of the annotation on the input VCF data   
- `run_annotation.sh`: the shell script to run either the annotation or the downloader, by default run the test annotation.    
- `vcf_annotation.py`: the python script to perform annotation, with optional arguments for input and/or output paths
- `utilities.py`: utility functions supporting the annotation program  
- `sequence_ontology.csv`: the sequence ontology table downloaded using the downloader program, necessary for the annotation program 
- `download_sequence_ontology.py`: the script to download the sequence ontology   
- `chromedriver`: the web driver needed to run the sequence ontology downloader   
- `README.md`: *this* document  




