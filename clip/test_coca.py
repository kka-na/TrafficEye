import open_clip
import torch
from PIL import Image

mpath = '/home/kana/Documents/Training/TrafficEye/clip/open_clip/src/logs/2023_11_07-13_29_04-model_RN50-lr_0.001-b_64-j_12-p_amp/checkpoints/epoch_220.pt'
model, _, transform = open_clip.create_model_and_transforms(
  model_name="RN50",
  pretrained=mpath
)

img_path ='/home/kana/Documents/Dataset/TS/test_data/DA_00S_HI_210918_02_002612.jpg'
im = Image.open(img_path).convert("RGB")
im = transform(im).unsqueeze(0)

with torch.no_grad(), torch.cuda.amp.autocast():
  generated = model.generate(im)

print(open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))