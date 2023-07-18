import os
import sys
import re
import math
import pprint
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import mysql.connector

import sqlalchemy
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)


#######################################################################
# Parse arguments
#######################################################################
parser = argparse.ArgumentParser(prog='upload_motif_sequence', description='upload_motif_sequence')

parser.add_argument('-c', '--chromosome', help='Chromosome', type=str, required=True)

args = parser.parse_args()

chromosome = args.chromosome


#######################################################################
# Connect database
#######################################################################
try:
    password = ''
except Exception as error:
    print('ERROR', error)

connection_string = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
    user='',
    password=password,
    host='127.0.0.1',
    database='KBC_Osativa'
)

engine = create_engine(connection_string, echo=True)
print(engine)

# connection = engine.connect()
# print(connection)


#######################################################################
# Read GFF file
#######################################################################
input_file_path = Path('/data/yenc/projects/2022_08_11_mViz_KBC/2022_08_11_upload_rice_gff/output/mViz_Rice_Nipponbare_GFF.txt')

gff_array = []
with open(input_file_path, "r") as reader:
    header = reader.readline()
    header_array = str(header).strip("\n").strip("\r").strip("\r\n").split("\t")
    for line in reader:
        line_array = str(line).strip("\n").strip("\r").strip("\r\n").split("\t")
        if str(line_array[0]) == str(chromosome):
            gff_array.append(line_array)


#######################################################################
# Delete in gene records
#######################################################################
output_table = "mViz_Rice_Japonica_" + chromosome + "_Motif_Sequence"
try:
    with engine.connect() as connection:
        condition_array = []
        for i in range(len(gff_array)):
            condition_array.append(
                "(Chromosome = '" + chromosome + "' AND Start >= " + str(int(gff_array[i][3])+500) + " AND End <= " + str(int(gff_array[i][4])-500) + ")"
            )
            if len(condition_array) > 5:
                sql_str = "DELETE FROM " + output_table + " WHERE " + " OR ".join(condition_array) + ";"
                result = connection.execute(sql_str)
                # print(sql_str)
                condition_array.clear()
        if len(condition_array) > 0:
            sql_str = "DELETE FROM " + output_table + " WHERE " + " OR ".join(condition_array) + ";"
            result = connection.execute(sql_str)
            # print(sql_str)
            condition_array.clear()
except Exception as e:
    print("Indexing position is not working.")
    print(e)
    sys.exit(1)
