from PIL import Image


def create_solid_color_image(width, height, color, output_path):
  # Create a new image with the specified size and color
  img = Image.new("RGB", (width, height), color)

  # Save the image
  img.save(output_path, "PNG")
  print(f"Saved {width}x{height} image to {output_path}")


# Usage
# Change '#7F00FF' to any hex code or color name you want
create_solid_color_image(3000, 3000, "#FFA500", "solid_orange_3000x3000.png")
