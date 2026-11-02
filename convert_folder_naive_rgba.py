import os
from PIL import Image


def convert_folder_normalized_rgba(input_folder, output_folder):
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  valid_extensions = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

  for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_extensions):
      input_path = os.path.join(input_folder, filename)
      base_name = os.path.splitext(filename)[0]
      output_path = os.path.join(output_folder, f"{base_name}.png")

      try:
        # Open image and extract pixel data
        img = Image.open(input_path).convert("RGBA")
        pixels = list(img.getdata())

        # --- Pass 1: Find the darkest value (minimum grayscale) ---
        # Pure white = 255, Pure black = 0
        min_gray = 255
        for r, g, b, _ in pixels:
          gray = (int(r) + int(g) + int(b)) / 3.0
          if gray < min_gray:
            min_gray = gray

        # Safety check: If the image is completely white, skip normalization math
        if min_gray >= 255:
          min_gray = 254

        # Calculate the dynamic range of our drawing (from darkest ink to white background)
        gray_range = 255.0 - min_gray

        # --- Pass 2: Normalize Alpha and scale up RGB values ---
        new_pixels = []
        for r, g, b, _ in pixels:
          gray = (int(r) + int(g) + int(b)) / 3.0

          # 1. Normalize Alpha: Pure white becomes 0, darkest value becomes 255
          # Formula: (255 - current_gray) / range * 255
          alpha_factor = (255.0 - gray) / gray_range
          new_alpha = int(alpha_factor * 255)
          new_alpha = max(0, min(255, new_alpha))

          # 2. Scale up RGB values:
          # Transparency darkens pixels visually. To counter this, we divide by the
          # alpha factor to restore original color intensity at that opacity level.
          if alpha_factor > 0:
            new_r = max(0, min(255, int(r / alpha_factor)))
            new_g = max(0, min(255, int(g / alpha_factor)))
            new_b = max(0, min(255, int(b / alpha_factor)))
          else:
            new_r, new_g, new_b = 255, 255, 255  # Fully transparent pixels

          new_pixels.append((new_r, new_g, new_b, new_alpha))

        # Rebuild and save the normalized image
        img.putdata(new_pixels)
        img.save(output_path, "PNG")
        print(f"Normalized & Saved: {filename}")

      except Exception as e:
        print(f"Error processing {filename}: {e}")


# Usage
source_dir = "./1101232530"
destination_dir = "./1101232530_naive_rgba"

convert_folder_normalized_rgba(source_dir, destination_dir)
