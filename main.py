import os
import zipfile

import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#  https://tomaugspurger.github.io/modern-1-intro.html

if int(os.environ.get("MODERN_PANDAS_EPUB", 0)):
    import prep

import requests

headers = {
    'Referer': 'https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time',
    'Origin': 'https://www.transtats.bts.gov',
    'Content-Type': 'application/x-www-form-urlencoded',
}

params = (
    ('Table_ID', '236'),
    ('Has_Group', '3'),
    ('Is_Zipped', '0'),
)

with open('modern-1-url.txt', encoding='utf-8') as f:
    data = f.read().strip()

os.makedirs('data', exist_ok=True)
dest = "data/flights.csv.zip"

if not os.path.exists(dest):
    r = requests.post('https://www.transtats.bts.gov/DownLoad_Table.asp',
                      headers=headers, params=params, data=data, stream=True)

    with open("data/flights.csv.zip", 'wb') as f:
        for chunk in r.iter_content(chunk_size=102400):
            if chunk:
                f.write(chunk)

zf = zipfile.ZipFile("data/flights.csv.zip")
fp = zf.extract(zf.filelist[0].filename, path='data/')
df = pd.read_csv(fp, parse_dates=["FL_DATE"]).rename(columns=str.lower)

print(df.info())

print(df.ix[10:15, ['fl_date', 'tail_num']])

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

first = df.groupby('airline_id')[['fl_date', 'unique_carrier']].first()
print(first.head())
