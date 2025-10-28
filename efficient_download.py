#!/usr/bin/env python3
"""
Efficient Image Downloader
Downloads sample images from smaller datasets or uses existing images
"""

import os
import requests
import urllib.request
from pathlib import Path
import time

def download_sample_images_from_web():
    """Download sample aesthetic images from free sources"""
    
    # Generate 100 high-quality images from Lorem Picsum (free placeholder images)
    sample_urls = []
    
    # Different sizes and orientations for variety
    sizes = [
        (800, 600),   # Landscape
        (600, 800),   # Portrait  
        (1000, 600),  # Wide
        (600, 1000),  # Tall
        (900, 700),   # Square-ish
        (700, 900),   # Square-ish portrait
    ]
    
    # Generate 100 URLs with different sizes
    for i in range(1, 101):
        size = sizes[i % len(sizes)]  # Cycle through different sizes
        url = f"https://picsum.photos/{size[0]}/{size[1]}?random={i}"
        sample_urls.append(url)
    
    # Create output directory
    output_dir = Path("my_100_images")
    output_dir.mkdir(exist_ok=True)
    
    print(f"Downloading {len(sample_urls)} sample images to {output_dir}/")
    print("Using Lorem Picsum (free high-quality images)")
    
    successful_downloads = 0
    
    for i, url in enumerate(sample_urls, 1):
        try:
            print(f"  Downloading image {i}/{len(sample_urls)}...", end=" ")
            
            # Download the image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Save the image
            filename = f"sample_image_{i:03d}.jpg"
            filepath = output_dir / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"OK {filename}")
            successful_downloads += 1
            
            # Small delay to be respectful to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    print(f"\nSuccessfully downloaded {successful_downloads} images!")
    return successful_downloads > 0

def copy_more_from_good_images():
    """Copy and rename existing images to create more variety"""
    
    good_images_dir = Path("GoodImages")
    output_dir = Path("my_100_images")
    output_dir.mkdir(exist_ok=True)
    
    if not good_images_dir.exists():
        return False
    
    # Find existing images
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    existing_images = [
        f for f in good_images_dir.iterdir() 
        if f.suffix.lower() in extensions
    ]
    
    if not existing_images:
        return False
    
    print(f"Found {len(existing_images)} images in GoodImages folder")
    print(f"Copying them to {output_dir}/ with new names")
    
    for i, img_file in enumerate(existing_images, 1):
        try:
            # Create new filename
            new_filename = f"good_image_{i:03d}{img_file.suffix}"
            new_filepath = output_dir / new_filename
            
            # Copy the file
            import shutil
            shutil.copy2(img_file, new_filepath)
            print(f"  Copied {img_file.name} → {new_filename}")
            
        except Exception as e:
            print(f"  Error copying {img_file.name}: {e}")
    
    return True

def main():
    """Main function to efficiently get sample images"""
    
    print("Efficient Image Downloader")
    print("=" * 50)
    print("This approach avoids downloading 30GB datasets!")
    print()
    
    # Strategy 1: Use existing images
    print("Strategy 1: Using existing images...")
    if copy_more_from_good_images():
        print("Successfully copied existing images")
    else:
        print("No existing images found in GoodImages folder")
    
    print()
    
    # Strategy 2: Download sample images from free source
    print("Strategy 2: Downloading sample images from web...")
    if download_sample_images_from_web():
        print("Successfully downloaded sample images")
    else:
        print("Failed to download sample images")
    
    print()
    
    # Check final result
    output_dir = Path("my_100_images")
    if output_dir.exists():
        image_files = [f for f in output_dir.iterdir() if f.suffix.lower() in {'.jpg', '.jpeg', '.png'}]
        print(f"Final Result: {len(image_files)} images in {output_dir}/")
        
        if len(image_files) > 0:
            print("\nReady to generate bad crops!")
            print("Next step: Run the bad crop generator on these images")
            print(f"Command: python simple_bad_crop.py")
        else:
            print("No images available for processing")
    
    print("\nDisk space used: Only a few MB")

if __name__ == "__main__":
    main()