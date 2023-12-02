import pandas as pd
import os
import random

base = '/home/kana/Documents/Dataset/TS'
folder_path = f"{base}/data256"  
jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
future_df = {"filepath":[], "title":[]}
rand_jpg_files = random.sample(jpg_files, 10000)

time_mapping = {'SS': 'sunset', 'DA': 'day', 'NI': 'night'}
weather_mapping = {'00S':'sunny', '00C':'cloudy', '00R':'rainy', '00F':'foggy', '0SC':'partly_sunny'}
road_mapping = {'HI':'highway', 'NO':'normal', 'TE':'tunnel', 'AC':'normal', 'BA':'back', 'FA':'normal', 'PR':'provincial', 'RO':'normal'}



for file_name in rand_jpg_files:
  parts = file_name.split('_')
  time = parts[0]
  weather = parts[1]
  road = parts[2]
  mtime = time_mapping.get(time, time)
  mweather = weather_mapping.get(weather, weather)
  mroad = road_mapping.get(road, road)
  caption = f"{mweather} {mroad} {mtime}"
  
  fname = file_name.split('.')[0]
  future_df["filepath"].append(f"{base}/data256/{file_name}")
  future_df["title"].append(caption)

pd.DataFrame.from_dict(future_df).to_csv(
  os.path.join(base, "ts_10000.csv"), index=False, sep="\t"
)