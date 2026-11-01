import os
from PIL import Image, ImageChops 


def overlay_drawings_on_background(
    drawings_folder, background_path, output_folder
):
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  # Load your new background image
  bg_image = Image.open(background_path).convert("RGBA")

  valid_extensions = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

  for filename in os.listdir(drawings_folder):
    if filename.lower().endswith(valid_extensions):
      drawing_path = os.path.join(drawings_folder, filename)
      output_path = os.path.join(output_folder, filename)

      try:
        # Open drawing and resize background to match it exactly
        drawing = Image.open(drawing_path).convert("RGBA")
        current_bg = bg_image.resize(drawing.size)

        # Multiply blend mode: White disappears, dark purple stays
        result = ImageChops.multiply(drawing, current_bg)

        result.save(output_path)
        print(f"Composited: {filename}")

      except Exception as e:
        print(f"Error processing {filename}: {e}")


# Usage
overlay_drawings_on_background(
    "./1101232530", "./solid_orange_3000x3000.png", "./1101232530_updated"
)
