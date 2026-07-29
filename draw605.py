from PIL import Image, ImageDraw, ImageFont
import numpy as np

def get_605_mask(w, h): 
    # Create a black grayscale image
    #w, h = 1000, 500
    img = Image.new("L", (w, h), color=0)  # "L" = 8-bit grayscale

    draw = ImageDraw.Draw(img)

    # Load a font (or use ImageFont.load_default())
    font = ImageFont.truetype("BAUHS93.TTF", 500)

    text = "605"

    # Center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (w - text_w) // 2
    y = (h - text_h) // 2

    # Draw white text
    draw.text((x, y-(h//5)), text, fill=255, font=font)

    #img.show() 

    # Convert to NumPy and scale to [0, 10001]
    arr = np.asarray(img, dtype=np.float32)
    #arr = np.round(arr / 255.0 * 10001).astype(np.int64)

    #print(arr.shape, arr.min(), arr.max())
    
    return (arr > 0) 
