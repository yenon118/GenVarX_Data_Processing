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
    database='KBC_Osativa'
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
        result = connection.execute("DROP TABLE IF EXISTS mViz_Rice_Japonica_TF CASCADE;")
except Exception as e:
    print("It is not working.")
    sys.exit(1)

folder_path = Path("/data/yenc/projects/2022_08_11_mViz_KBC/2022_08_11_upload_processed_rice_TF/output")
file_path = folder_path.joinpath('Osj_TF_list.txt')


if str(file_path).endswith('csv'):
    dat = pd.read_csv(
        filepath_or_buffer=file_path
    )
elif str(file_path).endswith('txt'):
    dat = pd.read_table(
        filepath_or_buffer=file_path,
        sep="\t"
    )

dat = dat.sort_values(by=['TF'])

dat.to_sql(
    name='mViz_Rice_Japonica_TF',
    chunksize=1000,
    con=engine,
    if_exists='append',
    index=False,
    schema='KBC_Osativa',
    dtype={
        "TF": sqlalchemy.types.VARCHAR(length=250)
    }
)
