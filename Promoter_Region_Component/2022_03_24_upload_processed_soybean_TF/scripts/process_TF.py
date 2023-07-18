#!/usr/bin/env python3

# python3 /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/scripts/process_TF.py \
# -i /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/data/Gma_TF_list.txt \
# -o /data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/output/Gma_TF_list.txt

import sys
import os
import re
import argparse
import pathlib
import gzip

import pandas as pd


# Process data
def process_line(line_array, output_array):
    tf = str(line_array[1]).strip()
    tf_family = str(line_array[2]).strip()

    output_array.append(
        tf + "\t" + 
        tf_family + "\n"
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
                process_line(line_array, output_array)
                # Write data
                if (len(output_array) > 0):
                    with open(output_file_path, 'a') as writer:
                        writer.write("".join(output_array))
                        output_array.clear()
    else:
        with open(input_file_path, "r") as reader:
            header = reader.readline()
            for line in reader:
                line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
                process_line(line_array, output_array)
                # Write data
                if (len(output_array) > 0):
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
    parser = argparse.ArgumentParser(prog='process_TF', description='process_TF')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
