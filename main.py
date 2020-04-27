import json
import pandas as pd
import numpy as np
import math

#open the json file and check if it is valid. If the file can be opened, its a valid json file
with open('geo.json') as geo_file:
  geo = json.load(geo_file)

with open('data.json') as data_file:
  data = json.load(data_file)

# create the geo dataframe and do necessary modifications to be able to work with latitude and longitude data
dfGeo = pd.DataFrame(geo)
dfGeo = pd.concat([dfGeo['ipv4'], dfGeo['geo'].str.split(',', expand=True)], axis=1, sort=False)
dfGeo.rename(columns={0:'lat',1:'lon'}, inplace=True)
dfGeo[['lat', 'lon']]=dfGeo[['lat','lon']].astype(float)

# validity test to see whether the latitude falls within -90,90 and the longitude falls within -180,180. If no dataframe is given, all the values are correct
dfLatLongCheck = dfGeo.loc[((dfGeo['lat']<-90) | (dfGeo['lat']>90)) | (dfGeo['lon']<(-180)) | (dfGeo['lon']>180)]
print (dfLatLongCheck)

dfData = pd.DataFrame(data)

# function to get the sorted data.json data according to euclidean distance for a given latitude and longitude
def euc_dist(latitude, longitude):
  dfData['euclidean'] = 6378 * 2 * np.arcsin(np.sqrt(np.sin((np.radians(dfGeo['lat']-math.radians(latitude)))/2)**2 + np.cos(math.radians(latitude))*np.cos(np.radians(dfGeo['lat'])) * np.sin((np.radians(dfGeo['lon']) - math.radians(longitude))/2)**2))
  dfDataSorted = dfData.sort_values(['euclidean'], ascending=[True])
  dfDataSorted.drop('euclidean', axis=1, inplace=True)
  dfDataSorted.to_json('sorted_data', orient='records')
  return dfDataSorted
  
# function to return the shortest distance data for given latitude and longitude in data.json
def shortest_euc_dist(latitude, longitude):
  df = euc_dist(latitude, longitude)
  return df.iloc[0,:]
