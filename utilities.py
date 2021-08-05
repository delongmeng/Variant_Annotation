'''
Utility functions supporting the vcf_annotation program.
'''

import requests
import pandas as pd
import argparse


def get_input_args():
    '''
    This function parses the arguments from user input. 
    ''' 

    # Create Parse using ArgumentParser
    parser = argparse.ArgumentParser()
    
    # Create command line arguments as mentioned above using add_argument() from ArguementParser method
    parser.add_argument('--input_path', type = str, default = "Challenge_data_(1).vcf",
                    help = 'Please define the input path (the default is: Challenge_data_(1).vcf)')
    parser.add_argument('--output_path', type = str, default = "output.tsv",
                    help = 'Please define the output path (the default is: output.tsv)')

    return parser.parse_args()   



def variant_process(variables, line):
    '''
    This function processes a line of data into a dictionary format for each variant.
    Returns the variant.
    '''

    # extract values and combine with the variable names in a dictionary
    values = line.strip("\n").split("\t")
    variant = dict(zip(variables, values))

    # the variable "INFO" contains multiple pieces of information, so convert it to a dictionary
    variant_info = {}
    for item in variant["INFO"].split(";"):
        key, value = item.split("=")
        variant_info[key] = value
    variant["INFO"] = variant_info

    # extract variable names under "FORMAT" so that we can map that to the data for the samples here: normal and vaf5
    format_keys = variant["FORMAT"].split(":")
    variant["normal"] = dict(zip(format_keys, variant["normal"].split(":")))
    variant["vaf5"] = dict(zip(format_keys, variant["vaf5"].split(":")))

    return variant



def get_af_effects(variant):
    '''
    This function takes a variant as an input, extracts and returns allele frequency and effect information from ExAC API.
    '''

    # Note that there might be multiple alternate alleles, so we split the data into a list
    alts = variant["ALT"].split(',')
    
    # set up empty lists to store the data for all the alleles
    effects = []
    allele_freqs = []

    # iterate through each allele and extract allele frequency and effect information from ExAC
    for alt in alts:

        # if the extraction fails, we will use '-' to indicate the data is not available
        allele_freq = '-'    
        effect = '-'

        # set up the base url and variant_id according to the instruction of ExAC API
        url_base = "http://exac.hms.harvard.edu/rest/variant/variant/"
        variant_id = ("-").join([variant["CHROM"], variant["POS"], variant["REF"], alt])

        # use a try-except-finally structure to handle potential error during the request
        try:
            # extract the allele frequency from the response (in json format)
            response = requests.get(url_base+variant_id).json()
            allele_freq = str(round(response["allele_freq"],4))

            '''
            Next we'll extract the effect (missense, silent, intergenic, etc.) of each allele from the "vep_annotations" element.
            Note that there could be multiple effects for each allele, and we will annotate with the most deleterious possibility.
            We extract all the effects from ExAC, and then determine the most deleterious one according to the severeness scores.
            Because the score range in our table is 0-35, setting a minimum score to be 36 will ensure any effect we can get will replace this value.
            Iterate through the vep_annotations, extract the "major_consequence", get the lowest score possible, and extract the effect using that score.
            '''
            min_score = 36
            for vep_annotation in response["vep_annotations"]:
                if vep_annotation["major_consequence"] in so_to_score:
                    score = so_to_score[vep_annotation["major_consequence"]]
                    if score < min_score:
                        min_score = score
            if min_score in score_to_so:
                effect = score_to_so[min_score]

        # no further process needed if we encounter an error
        except Exception:
            pass

        # append allele frequency and effect of the current allele to the lists
        finally:
            allele_freqs.append(allele_freq)    
            effects.append(effect) 

    return allele_freqs, effects



def annotate(input_path, output_path, variables_to_add, so_to_score, score_to_so):

    # open input and output files
    input_data = open(input_path, "r") 
    output = open(output_path, "w")

    # read each line of input data and process it accordingly
    for line in input_data:

        # for the annotation lines above the header, just keep them the same in the output
        if line.startswith("##"):
            output.write(line)

        # for the header line
        elif line.startswith("#"):
            # extract variable names so we can use them to easily access the data
            variables = line.strip("#\n").split("\t")
            # save the original variable names, plus the extra column names of the annotations that we'll add, to the output 
            output.write(line.strip("\n")+"\t"+"\t".join(variables_to_add)+"\n")

        # for all the data entries
        else:

            # we first reformat the data by storing it into a dictionary and also convert some of the element into dictionaries
            variant = variant_process(variables, line)

            # Extract the type of variation (substitution, insertion, CNV, etc.) 
            type_variation = variant["INFO"]["TYPE"]
            
            # Extract the depth of sequence coverage at the site of variation from "DP".
            normal_DP = int(variant["normal"]["DP"])
            vaf5_DP = int(variant["vaf5"]["DP"])

            # AO: Alternate allele observation count
            # Note that because there could be multiple alleles, we split the data and will get a list.
            normal_AO = variant["normal"]["AO"].split(',')
            vaf5_AO = variant["vaf5"]["AO"].split(',')    

            # RO: Reference allele observation count
            normal_RO = int(variant["normal"]["RO"])
            vaf5_RO = int(variant["vaf5"]["RO"])   
              
            # Calculate the percentage of both alternate allele(s) and reference allele for both "normal" and "vaf5" samples
            # Note that the result for the alternate allele(s) are lists. All results are converted to strings.
            normal_alt_perc = [str(round(int(num)/normal_DP, 4)) for num in normal_AO]
            normal_ref_perc = str(round(normal_RO/normal_DP, 4))
            vaf5_alt_perc = [str(round(int(num)/vaf5_DP, 4)) for num in vaf5_AO]
            vaf5_ref_perc = str(round(vaf5_RO/vaf5_DP, 4))

            
            # extracts allele frequency and the most deleterious possibile effect information from ExAC API for each alternate allele
            allele_freqs, effects = get_af_effects(variant)

            # combine all of the data together in a tab-seperated string 
            data_to_add = [type_variation, ",".join(effects), variant["normal"]["DP"], variant["vaf5"]["DP"],
                          variant["normal"]["AO"], variant["vaf5"]["AO"],",".join(normal_alt_perc),normal_ref_perc,
                           ",".join(vaf5_alt_perc),vaf5_ref_perc,",".join(allele_freqs)]

            # save the original data, plus the new annotation, into the output file
            output.write(line.strip("\n")+"\t"+"\t".join(data_to_add)+"\n")        

    # close input and output files
    input_data.close()
    output.close()

