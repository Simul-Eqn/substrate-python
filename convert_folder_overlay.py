import os
from PIL import Image, ImageOps


def mask_and_overlay(drawings_folder, background_path, output_folder):
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  bg_image = Image.open(background_path).convert("RGBA")
  valid_extensions = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

  for filename in os.listdir(drawings_folder):
    if filename.lower().endswith(valid_extensions):
      drawing_path = os.path.join(drawings_folder, filename)
      output_path = os.path.join(output_folder, filename)

      try:
        drawing = Image.open(drawing_path).convert("RGBA")
        current_bg = bg_image.resize(drawing.size)

        # Create a grayscale inversion to use as a mask
        # Pure white becomes 0 (transparent), darker colors become opaque
        grayscale = ImageOps.grayscale(drawing)
        alpha_mask = ImageOps.invert(grayscale)

        # Create a transparent version of the drawing using the mask
        transparent_drawing = drawing.copy()
        transparent_drawing.putalpha(alpha_mask)

        # Paste the transparent drawing onto the new background
        combined = Image.alpha_composite(current_bg, transparent_drawing)

        combined.save(output_path)
        print(f"Overlayed: {filename}")

      except Exception as e:
        print(f"Error processing {filename}: {e}")


# Usage
mask_and_overlay(
    "./1101232530", "./solid_orange_3000x3000.png", "./1101232530_overlay"
)
