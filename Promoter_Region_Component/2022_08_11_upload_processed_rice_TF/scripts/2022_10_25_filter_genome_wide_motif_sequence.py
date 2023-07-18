#!/usr/bin/env python3

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


upstream_length = 6000


# Process data
def process_line(line_array, gff_array, output_array):

    for i in range(len(gff_array)):
        if (str(line_array[0]).strip() == str(gff_array[i][0]).strip()) and \
        (int(str(line_array[3]).strip()) >= int(str(gff_array[i][11]).strip())) and \
        (int(str(line_array[4]).strip()) <= int(str(gff_array[i][12]).strip())):

            output_array.append(
                str(line_array[0]).strip() + "\t" + 
                str(line_array[1]).strip() + "\t" + 
                str(line_array[2]).strip() + "\t" + 
                str(line_array[3]).strip() + "\t" + 
                str(line_array[4]).strip() + "\t" + 
                str(line_array[5]).strip() + "\t" + 
                str(line_array[6]).strip() + "\t" + 
                str(line_array[7]).strip() + "\t" + 
                str(line_array[8]).strip() + "\t" + 
                str(line_array[9]).strip() + "\t" + 
                str(line_array[10]).strip() + "\n"
            )

            break


def main(args):
    #######################################################################
    # Get arguments
    #######################################################################
    input_file_path = args.input_file
    chromosome = args.chromosome
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
    # Read GFF file
    #######################################################################
    gff_array = []
    with open(reference_file_path, "r") as reader:
        header = reader.readline()
        header_array = str(header).strip("\n").strip("\r").strip("\r\n").split("\t")
        for line in reader:
            line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
            if line_array[0] == chromosome:
                if line_array[6] == "-":
                    promoter_start = int(line_array[4].strip())
                    promoter_end = promoter_start + upstream_length
                elif line_array[6] == "+":
                    promoter_end = int(line_array[3].strip())
                    promoter_start = promoter_end - upstream_length
                    if promoter_start < 0:
                        promoter_start = 0
                line_array.append(promoter_start)
                line_array.append(promoter_end)
                gff_array.append(line_array)

    print(gff_array[:6])
    print(gff_array[0][11])
    print(gff_array[0][12])

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

    with open(input_file_path, "r") as reader:
        for line in reader:
            line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
            if line_array[0] == chromosome:
                process_line(line_array, gff_array, output_array)
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

    dat = dat.sort_values(by=['Chromosome', 'Start', 'End', 'Name'])

    dat = dat.drop_duplicates(subset=['Chromosome', 'Source', 'Feature', 'Start', 'End', 'Strand', 'Name', 'Sequence'])

    dat = dat.sort_values(by=['Chromosome', 'Start', 'End', 'Name'])

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
    parser = argparse.ArgumentParser(prog='process_motif_sequence', description='process_motif_sequence')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-r', '--reference_file', help='Reference file', type=pathlib.Path, required=True)
    parser.add_argument('-c', '--chromosome', help='Chromosome', type=str, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
