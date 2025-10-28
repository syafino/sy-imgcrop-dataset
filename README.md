# Image Cropping Training Dataset Generator

### Essential Scripts
- **`efficient_download.py`** - Downloads 100 sample images efficiently 
- **`simple_bad_crop.py`** - Creates subtle bad crops with "Badcrop" prefix

### Configuration
- **`requirements.txt`** - Python dependencies
- **`kaggle.json`** - Kaggle API credentials (if using Kaggle datasets)

### Folders
- **`.venv/`** - Python virtual environment
- **`GoodImages/`** - Your original good images (if any)
- **`my_100_images/`** - Downloaded good images (104 total)
- **`bad_crops/`** - Generated bad crop versions

## Quick Usage

1. **Download 100 images:**
   ```bash
   python efficient_download.py
   ```

2. **Generate bad crops:**
   ```bash
   python simple_bad_crop.py
   ```
