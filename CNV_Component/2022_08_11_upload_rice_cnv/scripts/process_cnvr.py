#!/usr/bin/env python3

# python3 /data/yenc/projects/2022_03_24_mViz/2022_06_04_upload_cnv/scripts/process_cnvr.py \
# -i /data/yenc/projects/2022_03_24_mViz/2022_06_04_upload_cnv/data/cnvr.csv \
# -o /data/yenc/projects/2022_03_24_mViz/2022_06_04_upload_cnv/output/cnvr.txt

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


# Process data
def process_line(header_array, line_array, output_array):
    chromosome = str(line_array[0]).strip()
    start = str(line_array[1]).strip()
    end = str(line_array[2]).strip()
    width = str(line_array[3]).strip()
    strand = str(line_array[4]).strip()

    for i in range(5, len(header_array)):
        accession = str(header_array[i]).strip()
        cn_type = str(line_array[i]).strip()

        if (accession.endswith(".realigned.bam")):
            accession = re.sub("(\\.realigned\\.bam)", "", accession)
        
        accession = re.sub("\\.", "-", accession)

        output_array.append(
            chromosome + "\t" + 
            start + "\t" + 
            end + "\t" + 
            width + "\t" + 
            strand + "\t" + 
            accession + "\t" +
            cn_type + "\n"
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
        writer.write("Chromosome\tStart\tEnd\tWidth\tStrand\tAccession\tCN\n")

    #######################################################################
    # Process data
    #######################################################################
    chunksize = 10000
    output_array = []

    if str(input_file_path).endswith('gz'):
        with gzip.open(input_file_path, 'rt') as reader:
            header = reader.readline()
            header_array = str(header).strip("\n").strip("\r").strip("\r\n").split(",")
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split(",")
                process_line(header_array, line_array, output_array)
                # Write data
                if (len(output_array) > chunksize):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()
    else:
        with open(input_file_path, "r") as reader:
            header = reader.readline()
            header_array = str(header).strip("\n").strip("\r").strip("\r\n").split(",")
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split(",")
                process_line(header_array, line_array, output_array)
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
    parser = argparse.ArgumentParser(prog='process_cnvr', description='process_cnvr')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
