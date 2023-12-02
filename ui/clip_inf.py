import open_clip
import torch
from PIL import Image

m_base = '/home/kana/Documents/Training/TrafficEye/clip/open_clip/src/logs/'
m_dir = '2023_11_27-00_33_18-model_coca_ViT-B-32-lr_0.001-b_16-j_18-p_amp'
mpath = f'{m_base}/{m_dir}/checkpoints/best.pt'
model, _, transform = open_clip.create_model_and_transforms(
  model_name="coca_ViT-B-32",
  pretrained=mpath
)
img_path ='/home/kana/Documents/Dataset/TS/test_data/NI_00C_NO_211004_04_016892.jpg'


times = {'sunset', 'day', 'night'}
weathers = {'sunny', 'cloudy', 'rainy', 'foggy', 'partly_sunny'}
roads = {'highway', 'normal', 'tunnel', 'back', 'provincial'}


def get_result(file):
  im = Image.open(file).convert("RGB")
  im = transform(im).unsqueeze(0)

  with torch.no_grad(), torch.cuda.amp.autocast():
    generated = model.generate(im)

  caption = open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", "")
  caption = list(caption.split(' '))
  caption_unique = list(set(caption))

  t = 'time'
  w = 'weather'
  r = 'road'

  for cap in caption_unique:
    if cap in times:
      t = cap
    elif cap in weathers:
      w = cap
    elif cap in roads:
      r = cap

  c = f"Photo of a {w} {r} road at {t}"
  with open(f"{file.split('.')[0]}_cap.txt", 'w') as f:
    f.write(c)

  return c

#test
# c = get_result(img_path)
# print(c)