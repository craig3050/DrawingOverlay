import fitz  # PyMuPDF
from PIL import Image, ImageFilter
import numpy as np

def pdf_page_to_image(pdf_path, output_image_path, page_number=0, zoom=2):
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Check if the page exists
        if page_number >= len(pdf_document):
            print(f"Page {page_number} does not exist in the PDF.")
            return

        # Select the page
        page = pdf_document[page_number]

        # Define the zoom level (2x zoom for higher resolution)
        mat = fitz.Matrix(zoom, zoom)

        # Render the page to a pixmap (image representation)
        pix = page.get_pixmap(matrix=mat)

        # Save the pixmap as an image
        pix.save(output_image_path)
        print(f"Page {page_number} of the PDF has been saved as an image at {output_image_path}.")

        # Close the PDF document
        pdf_document.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def apply_blue_filter(image_path, output_path):
    try:
        # Open the image
        image = Image.open(image_path).convert("RGB")

        # Convert the image to a numpy array
        image_array = np.array(image)

        # Define a threshold for "white" pixels
        white_threshold = 240  # Adjust as needed
        is_white = np.all(image_array >= white_threshold, axis=-1)

        # Replace non-white pixels with blue
        image_array[~is_white] = [0, 0, 255]  # Blue color

        # Create a new image from the modified array
        blue_image = Image.fromarray(image_array)

        # Save the modified image
        blue_image.save(output_path)
        print(f"The filtered image has been saved at {output_path}.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
pdf_path = "Test1.pdf"  # Path to your PDF file
output_image_path = "output_image.png"  # Path to save the original image
filtered_image_path = "filtered_image.png"  # Path to save the filtered image

# Convert PDF page to image
pdf_page_to_image(pdf_path, output_image_path, page_number=0, zoom=2)

# Apply blue filter to the entire image
apply_blue_filter(output_image_path, filtered_image_path)
