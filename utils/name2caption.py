import os
import tarfile
from PIL import Image
from tqdm import tqdm

base = '/home/kana/Documents/Dataset/TS'

time_mapping = {'SS': 'sunset', 'DA': 'day', 'NI': 'night'}
weather_mapping = {'00S':'sunny', '00C':'cloudy', '00R':'rainy', '00F':'foggy', '0SC':'partly_sunny'}
road_mapping = {'HI':'highway', 'NO':'normal road', 'TE':'tunnel', 'AC':'normal road', 'BA':'back road', 'FA':'normal road', 'PR':'provincial road', 'RO':'normal road'}

folder_path = f"{base}/data"  
jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]

with tarfile.open(f'{base}/ts_tar.tar', 'w') as tarf:  
  for file_name in tqdm(jpg_files):
      parts = file_name.split('_')
      time = parts[0]
      weather = parts[1]
      road = parts[2]
      mtime = time_mapping.get(time, time)
      mweather = weather_mapping.get(weather, weather)
      mroad = road_mapping.get(road, road)

      caption = f"Photo of a {mweather} {mroad} at {mtime}"
      fname = file_name.split('.')[0]
      with open(f'{base}/caption/{fname}.txt', 'w') as c:
         c.write(caption)
      tarf.add(f'{base}/caption/{fname}.txt')

      img = Image.open(f"{folder_path}/{file_name}")
      img = img.resize((256, 256))
      img.save(f"{base}/data256/{fname}.jpg")