0684ecc5e22ca3f4c6f2983c03fb803c
#https://dev.to/m0nica/how-to-use-the-tmdb-api-to-find-films-with-the-highest-revenue-82p

import requests # to make TMDB API calls
import locale # to format currency as USD
locale.setlocale( locale.LC_ALL, '' )
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # to format currency on charts axis
import json # to manage json data
from datetime import datetime
# to handle  data retrieval
import urllib3
from urllib3 import request

# to handle certificate verification
import certifi

# for pandas dataframes
import pandas as pd
# handle certificate verification and SSL warnings
# https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl

http = urllib3.PoolManager(
       cert_reqs='CERT_REQUIRED',
       ca_certs=certifi.where())

# get data from the API: works fine for single movie data each time
url = 'https://api.themoviedb.org/3/movie/550?api_key=0684ecc5e22ca3f4c6f2983c03fb803c'
r = http.request('GET', url)
r.status
#The expected output of r.status is code 200 which means everything is OK.
## Implementation
#### II.1 setting and II.2 extract
import os, json
import numpy as np
import glob

movies=['550','551','552','553','554','555']
mydata=[]
for film in range(len(movies)):
    response = requests.get('https://api.themoviedb.org/3/movie/' + movies[film] + '?api_key=' + api_key)
    myjson = response.json()
    mydata.append(myjson)
    df = pd.DataFrame.from_dict(pd.json_normalize(mydata), orient='columns')

movies=df
movies.head(10)

#saving movies.csv file
movies.to_csv('C:/BI/Data Warehousing/Part 2/Lab 2/movies.csv', index=False, sep=',')

#### II.3.1 Transform

#creating list of selected columns
t_df=df[['budget', 'genres', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue', 'runtime']]
t_df.head(10)

#### II.3.2 Transformation 1
gen_df = pd.DataFrame()
for genre in t_df['genres']:
    for g in genre:
        gen_df = gen_df.append(g, ignore_index=True)
gen_df

#dropping duplicate category and round up ids
gen_df.id = gen_df.id.round(0).astype(int)
genres = gen_df.drop_duplicates()
genres

#saving genres.csv file
genres.to_csv('C:/BI/Data Warehousing/Part 2/Lab 2/genres.csv', index=False, sep=',')

#Generating column with frequency value
trans_g = gen_df.transpose().reset_index(drop=True)
freq_g = pd.DataFrame(trans_g.values[0:1], columns=trans_g.iloc[1])

freq_g

for header in freq_g:
    t_df[header] = "0"

for index, row in t_df.iterrows():
    for header in freq_g:
        gen = str(row["genres"]).lower()
        if gen.__contains__(str(header).lower()):
            row[header] = "1"
        else:
            row[header] = "0"
del t_df['genres']
genres_df = t_df
genres_df

#### II.3.2 Transformation 2

date_df = t_df[['id','release_date']]
date_df

#import pandas as pd
dt_index_obj = pd.DatetimeIndex(date_df['release_date'])
date_df['release_date'] = pd.to_datetime(date_df['release_date'])

# get day-month-year of the dateTimeIndex
date_df['day']=dt_index_obj.day
date_df['month']=dt_index_obj.month
date_df['year']=dt_index_obj.year
#get Weekdays of the date
date_df['Day_Of_Week'] = date_df['release_date'].dt.day_name()

datetimes=date_df
datetimes

#saving datetimes.csv file
datetimes.to_csv('C:/BI/Data Warehousing/Part 2/Lab 2/datetimes.csv', index=False, sep=',')

#### For VG

#convert runtime in hours and minutes
runtime_df = t_df[['id','runtime']]
runtime_df

from datetime import time

runtime_df['runtime'] = pd.to_datetime(runtime_df['runtime'], unit='s')
dt_index_obj = pd.DatetimeIndex(runtime_df['runtime'])

# get hours-minutes of the runtime
runtime_df['hours']=dt_index_obj.hour
runtime_df['minutes']=dt_index_obj.minute
runtime_df['seconds']=dt_index_obj.second

runtime_df


import pandas as pd
import sqlite3

conn = sqlite3.connect('test_database')
c = conn.cursor()

## Database For Movies dataframe
c.execute('CREATE TABLE IF NOT EXISTS movies (id, original_title, revenue)')
conn.commit()
df = pd.DataFrame(movies, columns=['id', 'original_title', 'revenue'])
df.to_sql('movies1', conn, if_exists='replace', index=False)

c.execute('''  
SELECT * FROM movies1
          ''')

for row in c.fetchall():
    print(row)

## Database For Genres dataframe

c.execute('CREATE TABLE IF NOT EXISTS genres (id, name)')
conn.commit()
gdf = pd.DataFrame(genres, columns=['id', 'name'])
gdf.to_sql('genres1', conn, if_exists='replace', index=False)

c.execute('''  
SELECT * FROM genres1
          ''')

for row in c.fetchall():
    print(row)

## Database For Datetimes dataframe

c.execute('CREATE TABLE IF NOT EXISTS datetimes (id, release_date)')
conn.commit()
ddf = pd.DataFrame(datetimes, columns=['id', 'release_date'])
ddf.to_sql('datetimes1', conn, if_exists='replace', index=False)

c.execute('''  
SELECT * FROM datetimes1
          ''')

for row in c.fetchall():
    print(row)

## Database For Runtime dataframe
c.execute('CREATE TABLE IF NOT EXISTS runtimes (id, runtime, hours, minutes, seconds)')
conn.commit()
ddf = pd.DataFrame(runtime_df, columns=['id', 'runtime', 'hours', 'minutes', 'seconds'])
ddf.to_sql('runtimes', conn, if_exists='replace', index=False)

c.execute('''  
SELECT * FROM runtimes
          ''')

for row in c.fetchall():
    print(row)
