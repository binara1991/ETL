import json
import requests
import config
import pandas as pd

api_key = config.api_key
# token = config.access_token
movies = ['550', '551', '552', '553', '554', '555']
mydata = []
mydata2 = []
mydata3 = []
mydata4 = []
for film in range(len(movies)):
    response = requests.get('https://api.themoviedb.org/3/movie/' + movies[film] + '?api_key=' + api_key)
    myjson = response.json()
    mydata.append(myjson)
    df = pd.DataFrame.from_dict(mydata)

# print(response)
# print(json.dumps(myjson, indent=4))
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 27)
# print(df)
# df.to_csv('test.csv')
for film in range(len(movies)):
    response = requests.get('https://api.themoviedb.org/3/movie/' + movies[film] + '?api_key=' + api_key)
    myjson = response.json()
    mydata2.append(myjson)
    # columns =['budget','genres','id','imdb_id','original_title','release_date', 'revenue','runtime']
    df2 = pd.DataFrame(mydata2,
                       columns=['budget', 'genres', 'id', 'imdb_id', 'original_title', 'release_date', 'revenue',
                                'runtime'])
# print(df2)
for film in range(len(movies)):
    response = requests.get('https://api.themoviedb.org/3/movie/' + movies[film] + '?api_key=' + api_key)
    myjson = response.json()
    mydata3.append(myjson['genres'])
    # columns =['budget','genres','id','imdb_id','original_title','release_date', 'revenue','runtime']
    #df3 =pd.DataFrame(mydata3).transpose()
    #df3.columns=['id','name']
    for i in range(len(mydata3)):
        df4 = pd.json_normalize(mydata3)
        print(df4)
        #mydata4.append(df4)

#print(df4)
