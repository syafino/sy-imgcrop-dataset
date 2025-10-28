#!/usr/bin/env python3
"""
Simple Bad Crop Generator
Creates one bad crop per image with "Badcrop" prefix
"""

import os
import random
import cv2
import numpy as np
from pathlib import Path
import sys

# All functionality is now self-contained in this file

def generate_subtle_bad_crop(image_path):
    """
    Generate a subtle bad crop - not obviously terrible, just poor composition
    
    Args:
        image_path: Path to input image
        
    Returns:
        Cropped image as numpy array
    """
    # Load image
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    h, w = image.shape[:2]
    
    # Choose from subtle bad cropping strategies
    strategies = [
        'slightly_off_center',
        'cut_bottom',
        'cut_top', 
        'cut_side',
        'awkward_but_not_extreme'
    ]
    
    strategy = random.choice(strategies)
    
    if strategy == 'slightly_off_center':
        # Crop that's just slightly off-center - looks almost good but isn't quite right
        crop_w = int(w * random.uniform(0.65, 0.8))  # Keep 65-80% of width
        crop_h = int(h * random.uniform(0.65, 0.8))  # Keep 65-80% of height
        
        # Position slightly off from center
        center_x, center_y = w // 2, h // 2
        offset_x = random.randint(-int(w * 0.1), int(w * 0.1))
        offset_y = random.randint(-int(h * 0.1), int(h * 0.1))
        
        x = max(0, min(w - crop_w, center_x - crop_w // 2 + offset_x))
        y = max(0, min(h - crop_h, center_y - crop_h // 2 + offset_y))
        
    elif strategy == 'cut_bottom':
        # Cut off bottom part (might miss feet, ground, etc.)
        crop_w = int(w * random.uniform(0.75, 0.9))
        crop_h = int(h * random.uniform(0.6, 0.75))  # Cut more from bottom
        
        x = random.randint(0, max(1, w - crop_w))
        y = 0  # Start from top
        
    elif strategy == 'cut_top':
        # Cut off top part (might miss heads, sky, etc.)
        crop_w = int(w * random.uniform(0.75, 0.9))
        crop_h = int(h * random.uniform(0.6, 0.75))
        
        x = random.randint(0, max(1, w - crop_w))
        y = h - crop_h  # Start from bottom
        
    elif strategy == 'cut_side':
        # Cut off one side
        crop_w = int(w * random.uniform(0.6, 0.75))
        crop_h = int(h * random.uniform(0.75, 0.9))
        
        y = random.randint(0, max(1, h - crop_h))
        if random.choice([True, False]):
            x = 0  # Cut from left
        else:
            x = w - crop_w  # Cut from right
            
    else:  # awkward_but_not_extreme
        # Slightly awkward aspect ratio but not extreme
        crop_w = int(w * random.uniform(0.6, 0.8))
        crop_h = int(h * random.uniform(0.6, 0.8))
        
        # Ensure it's not perfectly centered
        x = random.randint(int(w * 0.05), max(1, w - crop_w - int(w * 0.05)))
        y = random.randint(int(h * 0.05), max(1, h - crop_h - int(h * 0.05)))
    
    return image[y:y+crop_h, x:x+crop_w]

def create_simple_bad_crops(input_dir, output_dir):
    """
    Create one subtle bad crop per image with 'Badcrop' prefix
    
    Args:
        input_dir: Directory containing good images
        output_dir: Directory to save bad crops
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Supported image extensions
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    image_files = [
        f for f in input_path.iterdir() 
        if f.suffix.lower() in extensions
    ]
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return
    
    print(f"Found {len(image_files)} images to process...")
    print("Creating subtle bad crops (not obviously terrible, just poor composition)")
    
    successful_crops = 0
    
    for img_file in image_files:
        try:
            print(f"Processing: {img_file.name}")
            
            # Generate one subtle bad crop
            bad_crop = generate_subtle_bad_crop(img_file)
            
            # Create output filename with "Badcrop" prefix
            stem = img_file.stem
            suffix = img_file.suffix
            output_filename = f"Badcrop{stem}{suffix}"
            output_filepath = output_path / output_filename
            
            # Save the bad crop
            cv2.imwrite(str(output_filepath), bad_crop)
            print(f"  Created: {output_filename}")
            
            successful_crops += 1
            
        except Exception as e:
            print(f"  Error processing {img_file.name}: {e}")
            continue
    
    print(f"\nSuccessfully created {successful_crops} bad crops in '{output_dir}'")
    print(f"Files saved with 'Badcrop' prefix")

def main():
    """Main function"""
    input_dir = "my_100_images"
    output_dir = "bad_crops"
    
    print("Subtle Bad Crop Generator")
    print("=" * 40)
    print(f"Input: {input_dir}/")
    print(f"Output: {output_dir}/")
    print("Format: Badcrop[original_name][extension]")
    print("Creates subtle bad crops (~35% cropped, not obviously terrible)")
    print()
    
    # Check if input directory exists
    if not Path(input_dir).exists():
        print(f"Input directory '{input_dir}' not found!")
        print("Run the efficient_download.py script first to get images")
        return
    
    # Create bad crops
    create_simple_bad_crops(input_dir, output_dir)
    
    print("\nReady for training!")
    print(f"You now have:")
    print(f"   - Good images: {input_dir}/")
    print(f"   - Bad crops: {output_dir}/")

if __name__ == "__main__":
    main()