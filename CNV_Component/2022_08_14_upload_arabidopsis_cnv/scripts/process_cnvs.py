#!/usr/bin/env python3

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


# Process data
def process_line(line_array, output_array):
    accession = str(line_array[5]).strip()

    if (accession.endswith(".bam")):
        accession = re.sub("(\\.bam)", "", accession)

    output_array.append(
        str(line_array[0]).strip() + "\t" + 
        str(line_array[1]).strip() + "\t" + 
        str(line_array[2]).strip() + "\t" + 
        str(line_array[3]).strip() + "\t" + 
        str(line_array[4]).strip() + "\t" + 
        accession + "\t" + 
        str(line_array[6]).strip() + "\t" + 
        str(line_array[7]).strip() + "\t" + 
        str(line_array[8]).strip() + "\n"
    )


def main(args):
    #######################################################################
    # Get arguments
    #######################################################################
    input_file_path = args.input_file
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
    # Write output file header
    #######################################################################
    with open(output_file_path, 'w') as writer:
        writer.write("Chromosome\tStart\tEnd\tWidth\tStrand\tAccession\tMedian\tMean\tCN\n")

    #######################################################################
    # Process data
    #######################################################################
    chunksize = 10000
    output_array = []

    if str(input_file_path).endswith('gz'):
        with gzip.open(input_file_path, 'rt') as reader:
            header = reader.readline()
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split(",")
                process_line(line_array, output_array)
                # Write data
                if (len(output_array) > chunksize):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()
    else:
        with open(input_file_path, "r") as reader:
            header = reader.readline()
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split(",")
                process_line(line_array, output_array)
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
    parser = argparse.ArgumentParser(prog='process_cnvs', description='process_cnvs')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
