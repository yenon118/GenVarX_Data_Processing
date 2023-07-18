#!/usr/bin/env python3

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


# Process data
def process_line(line_array, reference_dict, output_array):
    chromosome = str(line_array[0]).strip()
    source = str(line_array[1]).strip()
    feature = str(line_array[2]).strip()
    start = str(line_array[3]).strip()
    end = str(line_array[4]).strip()
    score = str(line_array[5]).strip()
    strand = str(line_array[6]).strip()
    frame = str(line_array[7]).strip()
    description = str(line_array[8]).strip()

    gene_id = re.sub("(.*ID=)|(;.*)", "", description)
    gene_name = re.sub("(.*Name=)|(;.*)", "", description)
    gene_sequence = re.sub("(.*sequence=)|(;.*)", "", description)

    if gene_id.startswith('LOC_'):
        gene_id = re.sub("^LOC_", "", gene_id)
    if gene_name.startswith('LOC_'):
        gene_name = re.sub("^LOC_", "", gene_name)
    
    gene_id_split = gene_id.split('_')

    if chromosome == 'Chr1':
        chromosome = 'chr01'
    elif chromosome == 'Chr2':
        chromosome = 'chr02'
    elif chromosome == 'Chr3':
        chromosome = 'chr03'
    elif chromosome == 'Chr4':
        chromosome = 'chr04'
    elif chromosome == 'Chr5':
        chromosome = 'chr05'
    elif chromosome == 'Chr6':
        chromosome = 'chr06'
    elif chromosome == 'Chr7':
        chromosome = 'chr07'
    elif chromosome == 'Chr8':
        chromosome = 'chr08'
    elif chromosome == 'Chr9':
        chromosome = 'chr09'
    elif chromosome == 'Chr10':
        chromosome = 'chr10'
    elif chromosome == 'Chr11':
        chromosome = 'chr11'
    elif chromosome == 'Chr12':
        chromosome = 'chr12'

    if chromosome != 'ChrSy' and chromosome != 'ChrUn' and gene_id_split[0] in reference_dict.keys() and gene_name in reference_dict.keys():

        gene_id_split[0] = reference_dict[gene_id_split[0]]
        gene_id = '_'.join(gene_id_split)

        gene_name = reference_dict[gene_name]

        output_array.append(
            chromosome + "\t" + 
            source + "\t" + 
            feature + "\t" + 
            start + "\t" + 
            end + "\t" + 
            score + "\t" + 
            strand + "\t" + 
            frame + "\t" +
            gene_id + "\t" +
            gene_name + "\t" +
            gene_sequence + "\n"
        )


def main(args):
    #######################################################################
    # Get arguments
    #######################################################################
    input_file_path = args.input_file
    reference_file_path = args.reference_file
    output_file_path = args.output_file

    #######################################################################
    # Check if output parent folder exists
    # If not, create the output parent folder
    #######################################################################
    if not output_file_path.parent.exists():
        try:
            output_file_path.parent.mkdir(parents=True)
        except FileNotFoundError as e:
            pass
        except FileExistsError as e:
            pass
        except Exception as e:
            pass
        if not output_file_path.parent.exists():
            sys.exit(1)

    #######################################################################
    # Read reference
    #######################################################################
    reference_dict = {}
    with open(reference_file_path, 'r') as reader:
        header = reader.readline()
        for line in reader:
            line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
            if line_array[1] not in reference_dict.keys():
                reference_dict[line_array[1]] = line_array[0]

    #######################################################################
    # Write output file header
    #######################################################################
    with open(output_file_path, 'w') as writer:
        writer.write("Chromosome\tSource\tFeature\tStart\tEnd\tScore\tStrand\tFrame\tID\tName\tSequence\n")

    #######################################################################
    # Process data
    #######################################################################
    chunksize = 10000
    output_array = []

    if str(input_file_path).endswith('gz'):
        with gzip.open(input_file_path, 'rt') as reader:
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
                process_line(line_array, reference_dict, output_array)
                # Write data
                if (len(output_array) > chunksize):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()
    else:
        with open(input_file_path, "r") as reader:
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
                process_line(line_array, reference_dict, output_array)
                # Write data
                if (len(output_array) > chunksize):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()

    # Write data
    if (len(output_array) > 0):
        with open(output_file_path, 'a') as writer:
            writer.write("".join(output_array))
            output_array.clear()


if __name__ == "__main__":
    #######################################################################
    # Parse arguments
    #######################################################################
    parser = argparse.ArgumentParser(prog='process_rice_japonica', description='process_rice_japonica')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-r', '--reference_file', help='Reference file', type=pathlib.Path, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
