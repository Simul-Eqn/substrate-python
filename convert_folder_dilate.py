import os
import cv2
import numpy as np

# Define directories
input_folder = "1101232530_naive_rgba/"
output_folder = "1101232530_dilated"

os.makedirs(output_folder, exist_ok=True)
valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

# Smooth kernel for clean lines
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Read the image with unchanged channels (RGBA)
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        
        if img is not None:
            # --- STEP 1: FLATTEN RGBA ONTO TRUE BLACK ---
            if len(img.shape) == 3 and img.shape[2] == 4:
                height, width = img.shape[0], img.shape[1]
                black_bg = np.zeros((height, width, 3), dtype=np.uint8)
                
                bgr = img[:, :, :3]
                alpha_orig = img[:, :, 3]
                
                mask = alpha_orig / 255.0
                mask = np.expand_dims(mask, axis=2)
                
                img_to_dilate = (bgr * mask + black_bg * (1.0 - mask)).astype(np.uint8)
            else:
                img_to_dilate = img
            
            # --- STEP 2: APPLY DILATION ---
            dilated_bgr = cv2.dilate(img_to_dilate, kernel, iterations=1)
            
            # --- STEP 3: RECONSTRUCT RGBA ---
            # 1. Calculate the grayscale intensity of the dilated image
            gray = cv2.cvtColor(dilated_bgr, cv2.COLOR_BGR2GRAY)
            max_gray = np.max(gray)
            
            if max_gray > 0:
                # 2. Scale alpha so that max_gray becomes 255 opacity, black becomes 0
                alpha_new = ((gray / max_gray) * 255).astype(np.uint8)
                
                # 3. Scale up RGB values (un-multiply) to maintain vibrancy against transparent edges
                # Prevent division by zero by using np.where
                alpha_mask = alpha_new / 255.0
                alpha_mask_3d = np.expand_dims(alpha_mask, axis=2)
                
                # If alpha is greater than zero, scale the color up; otherwise, set to 0
                reconstructed_bgr = np.where(
                    alpha_mask_3d > 0, 
                    np.clip(dilated_bgr / alpha_mask_3d, 0, 255), 
                    0
                ).astype(np.uint8)
            else:
                # Fallback if the image is entirely pitch black
                alpha_new = np.zeros_like(gray)
                reconstructed_bgr = dilated_bgr
            
            # 4. Merge the adjusted BGR channels with the new alpha channel
            final_rgba = cv2.merge((reconstructed_bgr[:,:,0], 
                                    reconstructed_bgr[:,:,1], 
                                    reconstructed_bgr[:,:,2], 
                                    alpha_new))
            
            # --- STEP 4: SAVE AS RGBA PNG ---
            # Forced to save as .png to retain the 4th alpha channel natively
            output_png_path = os.path.splitext(output_path)[0] + ".png"
            cv2.imwrite(output_png_path, final_rgba)
            print(f"Processed with dynamic alpha: {os.path.basename(output_png_path)}")
        else:
            print(f"Could not read file: {filename}")

print("Batch processing complete! All images converted back to RGBA.")
