import fitz  # PyMuPDF
from PIL import Image
import numpy as np

class PDFToImageProcessor:
    def __init__(self, target_color=(0, 0, 255)):
        """
        Initializes the processor with the target recolor color.
        :param target_color: Tuple representing the RGB color to apply (default is blue).
        """
        self.target_color = target_color

    def set_target_color(self, color_name):
        """
        Sets the target color based on the color name.
        :param color_name: String representing the color (e.g., 'blue', 'red', 'green').
        """
        colors = {
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203),
            'yellow': (255, 255, 0)
        }
        self.target_color = colors.get(color_name.lower(), (0, 0, 255))  # Default to blue if color not found

    def pdf_page_to_image(self, pdf_path, page_number=0, zoom=2):
        """
        Converts a PDF page directly into a PIL image.
        :param pdf_path: Path to the PDF file.
        :param page_number: Page number to convert (0-based index).
        :param zoom: Zoom level for the image resolution.
        :return: PIL Image object of the page.
        """
        try:
            # Open the PDF file
            pdf_document = fitz.open(pdf_path)

            # Check if the page exists
            if page_number >= len(pdf_document):
                raise ValueError(f"Page {page_number} does not exist in the PDF.")

            # Select the page
            page = pdf_document[page_number]

            # Define the zoom level (2x zoom for higher resolution)
            mat = fitz.Matrix(zoom, zoom)

            # Render the page to a pixmap (image representation)
            pix = page.get_pixmap(matrix=mat)

            # Close the PDF document
            pdf_document.close()

            # Convert the pixmap to a PIL image
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            return image

        except Exception as e:
            raise RuntimeError(f"An error occurred while converting the PDF to an image: {e}")

    def recolor_image(self, image):
        """
        Recolors the non-white pixels of an image with the target color.
        :param image: PIL Image object.
        :return: Recolored PIL Image object.
        """
        try:
            # Convert the image to a numpy array
            image_array = np.array(image)

            # Define a threshold for "white" pixels
            white_threshold = 240  # Adjust as needed
            is_white = np.all(image_array >= white_threshold, axis=-1)

            # Replace non-white pixels with the target color
            image_array[~is_white] = self.target_color

            # Create a new image from the modified array
            recolored_image = Image.fromarray(image_array)
            return recolored_image

        except Exception as e:
            raise RuntimeError(f"An error occurred while recoloring the image: {e}")

    def process_pdf(self, pdf_path, page_number=0, zoom=2):
        """
        Processes a PDF page by converting it to an image and recoloring it.
        :param pdf_path: Path to the PDF file.
        :param page_number: Page number to process (0-based index).
        :param zoom: Zoom level for the image resolution.
        :return: Recolored PIL Image object.
        """
        image = self.pdf_page_to_image(pdf_path, page_number, zoom)
        return self.recolor_image(image)

# Example usage
if __name__ == "__main__":
    # Initialize the processor with the default color (blue)
    processor = PDFToImageProcessor()

    # Set a different color, e.g., 'red'
    processor.set_target_color("red")

    # Process the PDF and recolor the first page
    pdf_path = "Test1.pdf"  # Path to your PDF file
    recolored_image = processor.process_pdf(pdf_path, page_number=0, zoom=2)

    # Save the output image
    recolored_image.save("output_recolored_image.png")
    print("The recolored image has been saved as 'output_recolored_image.png'.")

# from DrawingColour import PDFToImageProcessor
#
# processor = PDFToImageProcessor()
# processor.set_target_color("green")  # Change to desired color
# recolored_image = processor.process_pdf("Test1.pdf", page_number=0)
# recolored_image.save("output.png")