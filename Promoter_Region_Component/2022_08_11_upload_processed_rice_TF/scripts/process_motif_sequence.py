#!/usr/bin/env python3

# python3 /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/scripts/process_motif_sequence.py \
# -i /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/data/Glycine_max_binding_TFBS_from_motif_inProm_Gma.gff \
# -o /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/output/Glycine_max_binding_TFBS_from_motif_inProm_Gma.txt

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


# Process data
def process_line(line_array, output_array):
    attributes = str(line_array[8]).strip()

    id = ""
    name = ""
    sequence = ""

    if (str(attributes).find("ID") != -1):
        id = re.sub("(.*ID=)|(;.*)", "", attributes)
    if (str(attributes).find("Name") != -1):
        name = re.sub("(.*Name=)|(;.*)", "", attributes)
    if (str(attributes).find("sequence") != -1):
        sequence = re.sub("(.*sequence=)|(;.*)", "", attributes)

    output_array.append(
        str(line_array[0]).strip() + "\t" + 
        str(line_array[1]).strip() + "\t" + 
        str(line_array[2]).strip() + "\t" + 
        str(line_array[3]).strip() + "\t" + 
        str(line_array[4]).strip() + "\t" + 
        str(line_array[5]).strip() + "\t" + 
        str(line_array[6]).strip() + "\t" + 
        str(line_array[7]).strip() + "\t" + 
        id + "\t" + 
        name + "\t" + 
        sequence + "\n"
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
                process_line(line_array, output_array)
                # Write data
                if (len(output_array) > chunksize):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()
    else:
        with open(input_file_path, "r") as reader:
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
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
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
