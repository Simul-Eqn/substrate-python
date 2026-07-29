from PIL import Image, ImageChops, ImageEnhance, ImageFilter
from pathlib import Path 
import os 

d = Path(__file__).parent/"222405" 
saved = d/"bloomed"
os.makedirs(saved,exist_ok=True)

def bloom(im, threshold=200, blurradius=15, boost=1.5): 
    mask = im.point(lambda p: 255 if p > threshold else 0)

    bloom_layer = mask.filter(ImageFilter.GaussianBlur(radius=blurradius))

    enhancer = ImageEnhance.Brightness(bloom_layer)
    bloom_boosted = enhancer.enhance(boost) 

    final_image = ImageChops.screen(im, bloom_boosted)

    return final_image 

for i in range(len(next(os.walk(d))[2])): 
    imgname = "{:03d}.png".format(i)
    img = Image.open(d/imgname).convert("RGB")
    final_image = bloom(img, boost=1.2) 
    final_image.save(saved/imgname)
