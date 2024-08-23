# SVS to PNG Conversion Script

This script converts SVS files to PNG format at both original resolution and a smaller resolution (e.g., 4K). The smaller version is useful for fine-tuning image adjustments, which can then be applied to the original high-resolution image.

## Requirements

- Python 3.x
- Pillow
- OpenSlide Python bindings

Install the required packages using pip:

```bash
pip install pillow openslide-python
```

## Usage

1. **Set File Paths:**
   - Modify the `file1_path` and `file2_path` variables in the script to point to your SVS files.
   - Adjust the output paths as needed.

2. **Run the Script:**
   - Execute the script to convert the SVS files to PNG format at both the original and 4K resolution.

```bash
python svs_to_png.py
```

3. **Output:**
   - The script will generate two PNG files for each SVS file:
     - The original resolution PNG.
     - The 4K resolution PNG (suffix `_min.png`).

4. **Audio Notification:**
   - A system sound will play when the conversion is complete.

## Example

```python
# Original file paths
file1_path = r"C:\svs\dosya1.svs"
file2_path = r"C:\svs\dosya2.svs"

# Output paths
output_path1 = r"C:\svs\output_image1.png"
min_output_path1 = r"C:\svs\output_image1_min.png"
output_path2 = r"C:\svs\output_image2.png"
min_output_path2 = r"C:\svs\output_image2_min.png"

# Convert SVS to PNG
convert_svs_to_png(file1_path, output_path1, min_output_path1)
convert_svs_to_png(file2_path, output_path2, min_output_path2)
```

## Notes

- The `resize_width` parameter is set to 3840 pixels for generating the 4K resolution images. You can adjust this value if needed.
- Ensure that the output paths have sufficient disk space, as the PNG files may be large.
