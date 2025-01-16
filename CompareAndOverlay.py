from DrawingColour import PDFToImageProcessor
from DrawingOverlay import ImageOverlay
from FileNameMatcher import FileNameMatcher
from PIL import Image
import os

# Example directories and sample filename
dir1 = "C:/Users/craig/Downloads/Compare3"
dir2 = "C:/Users/craig/Downloads/Compare2"
output_dir = "C:/Users/craig/Downloads/Compare4"
sample_filename = "1MC08-BBV_MSD-ME-DGA-NS01_NL01-250301.pdf"
# Define the transparency value
transparency = 0.5  # Adjust between 0 and 1 as needed

os.makedirs(output_dir, exist_ok=True)

def get_unique_filename(base_path, filename):
    """
    Generate a unique file name by appending (1), (2), etc. if the file already exists.
    """
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(base_path, unique_filename)):
        unique_filename = f"{base}({counter}){ext}"
        counter += 1
    return unique_filename

# STEP 1: Find Matching File Names
# Instantiate the matcher
matcher = FileNameMatcher(dir1, dir2, sample_filename)
# Find matches
matches = matcher.find_matches()
# Print matches
if matches:
    print("Matches found:")
    match_total = len(matches)
    print(f"There are {match_total} matches.")
    match_counter = 0
    for match in matches:
        match_counter += 1
        print(f"Match {match_counter} (of {match_total}): File1: {match[0]}, File2: {match[1]}")
        try:
            # Change match zero to colour blue
            # STEP 2: Process PDFs to a base colour
            processor = PDFToImageProcessor()
            processor.set_target_color("blue")  # Change to desired color
            image1_overlay = processor.process_pdf(f"{dir1}/{match[0]}", page_number=0)

            # Change match one to colour red
            processor = PDFToImageProcessor()
            processor.set_target_color("red")  # Change to desired color
            image2_overlay = processor.process_pdf(f"{dir2}/{match[1]}", page_number=0)

            # STEP 3: Overlay Images
            overlay_instance = ImageOverlay(image1_overlay, image2_overlay, transparency)
            # Call the overlay method to get the blended image
            blended_image = overlay_instance.overlay()

            # Get unique file name and save the blended image
            unique_filename = get_unique_filename(output_dir, f"{match[1]}.png")
            blended_image.save(os.path.join(output_dir, unique_filename))
            print(f"Blended image saved as: {unique_filename}")
        except Exception as e:
            print(e)

else:
    print("No matches found.")

print("Programme complete.")