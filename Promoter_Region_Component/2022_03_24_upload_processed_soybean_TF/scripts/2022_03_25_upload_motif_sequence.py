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


try:
    password = ''
except Exception as error:
    print('ERROR', error)

connection_string = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
    user='',
    password=password,
    host='127.0.0.1',
    database='soykb'
)

engine = create_engine(connection_string, echo=True)
print(engine)

# connection = engine.connect()
# print(connection)

try:
    with engine.connect() as connection:
        result = connection.execute("SELECT DATABASE();")
        for row in result:
            print(str(row))
        result = connection.execute("DROP TABLE IF EXISTS mViz_Soybean_" + chromosome + "_Motif_Sequence CASCADE;")
except Exception as e:
    print("It is not working.")
    sys.exit(1)

folder_path = Path("/data/yenc/projects/2022_03_24_mViz/2022_03_24_upload_processed_soybean_TF/output")
file_path = folder_path.joinpath('Glycine_max_binding_TFBS_from_motif_genome-wide_Gma.txt')


if str(file_path).endswith('csv'):
    dat = pd.read_csv(
        filepath_or_buffer=file_path
    )
elif str(file_path).endswith('txt'):
    dat = pd.read_table(
        filepath_or_buffer=file_path,
        sep="\t"
    )

dat = dat[dat["Chromosome"] == chromosome]

dat = dat.sort_values(by=['Chromosome', 'Start'])

dat.to_sql(
    name="mViz_Soybean_" + chromosome + "_Motif_Sequence",
    chunksize=1000,
    con=engine,
    if_exists='append',
    index=False,
    schema='soykb',
    dtype={
        "Chromosome": sqlalchemy.types.VARCHAR(length=50),
        "Source": sqlalchemy.types.VARCHAR(length=50),
        "Feature": sqlalchemy.types.VARCHAR(length=50),
        "Start": sqlalchemy.types.BIGINT,
        "End": sqlalchemy.types.BIGINT,
        "Score": sqlalchemy.types.VARCHAR(length=50),
        "Strand": sqlalchemy.types.VARCHAR(length=50),
        "Frame": sqlalchemy.types.VARCHAR(length=50),
        "ID": sqlalchemy.types.VARCHAR(length=250),
        "Name": sqlalchemy.types.VARCHAR(length=250),
        "Sequence": sqlalchemy.types.TEXT
    }
)

#######################################################################
# Index table
#######################################################################
output_table = "mViz_Soybean_" + chromosome + "_Motif_Sequence"
try:
    with engine.connect() as connection:
        sql_str = "CREATE INDEX " + output_table + "_chrom_idx ON " + output_table + "(Chromosome);"
        result = connection.execute(sql_str)
        # print(sql_str)
        sql_str = "CREATE INDEX " + output_table + "_start_idx ON " + output_table + "(Start);"
        result = connection.execute(sql_str)
        sql_str = "CREATE INDEX " + output_table + "_end_idx ON " + output_table + "(End);"
        result = connection.execute(sql_str)
        sql_str = "CREATE INDEX " + output_table + "_id_idx ON " + output_table + "(ID);"
        result = connection.execute(sql_str)
        sql_str = "CREATE INDEX " + output_table + "_name_idx ON " + output_table + "(Name);"
        result = connection.execute(sql_str)
        sql_str = "CREATE INDEX " + output_table + "_seq_idx ON " + output_table + "(Sequence(10));"
        result = connection.execute(sql_str)
except Exception as e:
    print("Indexing position is not working.")
    print(e)
    sys.exit(1)
