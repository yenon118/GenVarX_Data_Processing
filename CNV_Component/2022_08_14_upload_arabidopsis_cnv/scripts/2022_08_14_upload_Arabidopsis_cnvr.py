import os
import sys
import re
import math
import pprint
from pathlib import Path

import numpy as np
import pandas as pd

import mysql.connector

import sqlalchemy
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)

try:
    password = ''
except Exception as error:
    print('ERROR', error)

connection_string = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
    user='',
    password=password,
    host='127.0.0.1',
    database='KBC_Athaliana'
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
        result = connection.execute("DROP TABLE IF EXISTS mViz_Arabidopsis_CNVR CASCADE;")
except Exception as e:
    print("It is not working.")
    sys.exit(1)

folder_path = Path("/data/yenc/projects/2022_08_11_mViz_KBC/2022_08_14_upload_arabidopsis_cnv/output")
file_path = folder_path.joinpath('processed_cnvr.txt')


if str(file_path).endswith('csv'):
    dat = pd.read_csv(
        filepath_or_buffer=file_path
    )
elif str(file_path).endswith('txt'):
    dat = pd.read_table(
        filepath_or_buffer=file_path,
        sep="\t"
    )


dat.to_sql(
    name='mViz_Arabidopsis_CNVR',
    chunksize=1000,
    con=engine,
    if_exists='append',
    index=False,
    schema='KBC_Athaliana',
    dtype={
        "Chromosome": sqlalchemy.types.VARCHAR(length=250),
        "Start": sqlalchemy.types.BIGINT,
        "End": sqlalchemy.types.BIGINT,
        "Width": sqlalchemy.types.BIGINT,
        "Strand": sqlalchemy.types.VARCHAR(length=5),
        "Accession": sqlalchemy.types.VARCHAR(length=250),
        "CN": sqlalchemy.types.VARCHAR(length=10),
    }
)


# Index table
try:
    with engine.connect() as connection:
        sql_str = "CREATE INDEX mViz_Arabidopsis_CNVR_accession_idx ON mViz_Arabidopsis_CNVR(Accession);"
        result = connection.execute(sql_str)
        # print(sql_str)
        sql_str = "CREATE INDEX mViz_Arabidopsis_CNVR_start_idx ON mViz_Arabidopsis_CNVR(Start);"
        result = connection.execute(sql_str)
        # print(sql_str)
        sql_str = "CREATE INDEX mViz_Arabidopsis_CNVR_end_idx ON mViz_Arabidopsis_CNVR(End);"
        result = connection.execute(sql_str)
        # print(sql_str)
        sql_str = "CREATE INDEX mViz_Arabidopsis_CNVR_chromosome_idx ON mViz_Arabidopsis_CNVR(Chromosome);"
        result = connection.execute(sql_str)
        # print(sql_str)
except Exception as e:
    print("It is not working.")
    print(e)
    sys.exit(1)