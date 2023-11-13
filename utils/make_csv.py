import pandas as pd
import os

base = '/home/kana/Documents/Dataset/TS'
folder_path = f"{base}/data256"  
jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
future_df = {"filepath":[], "title":[]}
for file_name in jpg_files:
  fname = file_name.split('.')[0]

  with open(f'{base}/caption/{fname}.txt', 'r') as f:
    cap = f.read()
  
  future_df["filepath"].append(f"{base}/data256/{file_name}")
  future_df["title"].append(cap)

pd.DataFrame.from_dict(future_df).to_csv(
  os.path.join(base, "ts.csv"), index=False, sep="\t"
)