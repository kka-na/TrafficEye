import torch
from PIL import Image
import open_clip

base = '/home/kana/Documents/Dataset/TS'
mpath = '/home/kana/Documents/Training/TrafficEye/clip/open_clip/src/logs/2023_11_07-13_29_04-model_RN50-lr_0.001-b_64-j_12-p_amp/checkpoints/epoch_220.pt'
model, _, preprocess = open_clip.create_model_and_transforms('RN50', pretrained=mpath)
tokenizer = open_clip.get_tokenizer('RN50')

img_path ='/home/kana/Documents/Dataset/TS/test_data/DA_00S_HI_210918_02_002612.jpg'
image = preprocess(Image.open(img_path)).unsqueeze(0)
with open(f'{base}/possible_decriptions.txt','r', encoding='utf-8') as f:
  token_list = f.read().splitlines()
text = tokenizer(token_list)

with torch.no_grad(), torch.cuda.amp.autocast():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    print(image_features)
    print(text_features)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

print("Label probs:", text_probs)  # prints: [[1., 0., 0.]]

