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
    gene_id = str(line_array[1]).strip()
    tf_family = str(line_array[2]).strip()

    if gene_id.startswith('LOC_'):
        gene_id = re.sub("^LOC_", "", gene_id)
    
    if gene_id in reference_dict.keys():
        output_array.append(
            reference_dict[gene_id] + "\t" + 
            tf_family + "\n"
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
        writer.write("TF\tTF_Family\n")

    #######################################################################
    # Process data
    #######################################################################
    chunksize = 10000
    output_array = []

    if str(input_file_path).endswith('gz'):
        with gzip.open(input_file_path, 'rt') as reader:
            header = reader.readline()
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
            header = reader.readline()
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

    #######################################################################
    # Remove duplicate entries
    #######################################################################
    dat = pd.read_table(
        filepath_or_buffer=output_file_path
    )

    dat = dat.sort_values(by=['TF', 'TF_Family'])

    dat = dat.drop_duplicates()

    dat = dat.sort_values(by=['TF', 'TF_Family'])

    dat.to_csv(
        path_or_buf=output_file_path,
        sep='\t',
        index=False,
        doublequote=False,
        mode='w'
    )


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
