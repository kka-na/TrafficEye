times = {'sunset', 'day', 'night'}
weathers = {'sunny', 'cloudy', 'rainy', 'foggy', 'partly_sunny'}
roads = {'highway', 'normal road', 'tunnel', 'back road', 'provincial road'}

base = '/home/kana/Documents/Dataset/TS'
with open(f'{base}/possible_decriptions.txt', 'w') as f:
  for weather in weathers:
    for road in roads:
      for time in times:
        caption = f"a {weather} {road} at {time}\n"
        print(caption)
        f.write(caption)