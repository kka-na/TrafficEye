import tarfile
import os
from tqdm import tqdm
import webdataset as wds
import random

max_shard = 1000
base = '/home/kana/Documents/Dataset/TS'
folder_path = f"{base}/data256"  
jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
ll = len(jpg_files)//max_shard
random.seed(1)
suffled = random.sample(jpg_files, len(jpg_files))


#with tarfile.open(f'{base}/ts_tar.tar', 'w') as tarf:
with wds.ShardWriter(f'{base}/ts-%06d.tar', maxcount=max_shard) as sink:
    for i, file_name in tqdm(enumerate(suffled)):
        fname = file_name.split('.')[0]
        # tarf.add(f'{base}/caption/{fname}.txt', arcname=f'{fname}.txt')
        # tarf.add(f"{base}/data256/{fname}.jpg", arcname=f'{fname}.jpg')
        with open(f"{base}/data256/{fname}.jpg", 'rb') as image_file, open(f'{base}/caption/{fname}.txt', 'r') as text_file:
            image_data = image_file.read()
            text_data = text_file.read()

        key = f"ts-{i}"
        sample = {"__key__": key, "jpg": image_data, "txt": text_data}
        sink.write(sample)
