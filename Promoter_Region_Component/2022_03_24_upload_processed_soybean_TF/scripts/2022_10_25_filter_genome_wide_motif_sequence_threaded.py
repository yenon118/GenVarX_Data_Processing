#!/usr/bin/env python3

import sys
import os
import re
import argparse
import pathlib
import gzip
import collections

from queue import Queue
from threading import Thread

import pandas as pd


upstream_length = 6000
num_of_workers = 20


class Worker(Thread):
    def __init__(self, in_queue, out_queue, gff_array):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.gff_array = gff_array

    def run(self):
        while True:
            if self.in_queue:
                line_array = self.in_queue.popleft()
                if line_array == "EXIT":
                    break
                elif isinstance(line_array, (dict, list)):
                    for i in range(len(self.gff_array)):
                        if (str(line_array[0]).strip() == str(self.gff_array[i][0]).strip()) and \
                        (int(str(line_array[3]).strip()) >= int(str(self.gff_array[i][11]).strip())) and \
                        (int(str(line_array[4]).strip()) <= int(str(self.gff_array[i][12]).strip())):

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

                            self.out_queue.append(
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

                            break


class Recorder(Thread):
    def __init__(self, in_queue, output_file_path):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.output_file_path = output_file_path
        self.chunksize = 100000
        self.output_array = []

    def run(self):
        while True:
            if self.in_queue:
                output_str = self.in_queue.popleft()
                if output_str == "EXIT":
                    if (len(self.output_array) > 0):
                        with open(self.output_file_path, 'a') as writer:
                            writer.write("".join(self.output_array))
                            self.output_array.clear()
                    break
                else:
                    self.output_array.append(output_str)
                    if (len(self.output_array) > self.chunksize):
                        with open(self.output_file_path, 'a') as writer:
                            writer.write("".join(self.output_array))
                            self.output_array.clear()


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
    # Read GFF file
    #######################################################################
    gff_array = []
    with open(reference_file_path, "r") as reader:
        header = reader.readline()
        header_array = str(header).strip("\n").strip("\r").strip("\r\n").split("\t")
        for line in reader:
            line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
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
    # Create queues
    #######################################################################
    # in_queue = Queue()
    # out_queue = Queue()

    in_queue = collections.deque()
    out_queue = collections.deque()

    #######################################################################
    # Create workers
    #######################################################################
    worker_array = [None] * num_of_workers

    for i in range(num_of_workers):
        worker = Worker(in_queue, out_queue, gff_array)
        worker_array[i] = worker
    for i in range(num_of_workers):
        worker_array[i].daemon = True
        worker_array[i].start()
    
    recorder = Recorder(out_queue, output_file_path)
    recorder.daemon = True
    recorder.start()

    #######################################################################
    # Process data
    #######################################################################
    chunksize = 10000
    output_array = []

    with open(input_file_path, "r") as reader:
        for line in reader:
            line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
            in_queue.append(line_array)


    #######################################################################
    # Disable workers
    #######################################################################
    for i in range(num_of_workers):
        in_queue.append("EXIT")
    out_queue.append("EXIT")

    for i in range(num_of_workers):
        worker_array[i].join()
    recorder.join()

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
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
