from PIL import Image

class ImageOverlay:
    def __init__(self, image1, image2, transparency=0.5):
        """
        Initialize the ImageOverlay class with two image objects and a transparency value.

        Parameters:
            image1 (Image): First image object.
            image2 (Image): Second image object.
            transparency (float): Transparency level for blending (0 to 1).
                                  0 means fully image1, 1 means fully image2.
        """
        self.image1 = image1.convert("RGBA")
        self.image2 = image2.convert("RGBA")
        self.transparency = transparency

        # Ensure transparency is within the valid range
        if not (0 <= transparency <= 1):
            raise ValueError("Transparency must be between 0 and 1.")

        # Check if images are the same size
        if self.image1.size != self.image2.size:
            raise ValueError("Images must have the same dimensions.")

    def overlay(self):
        """
        Overlays the two images and returns the blended image object.

        Returns:
            Image: The blended image object.
        """
        # Blend the images
        blended = Image.blend(self.image1, self.image2, self.transparency)
        return blended

if __name__ == "__main__":
    # Example usage:
    # Open image objects
    image1 = Image.open("test3.png")  # Replace with your first image object
    image2 = Image.open("test4.png")  # Replace with your second image object

    # User-defined transparency value
    transparency = 0.5  # Adjust this value between 0 and 1 as needed

    # Create an instance of ImageOverlay
    overlay_instance = ImageOverlay(image1, image2, transparency)

    # Call the overlay method and get the blended image
    blended_image = overlay_instance.overlay()

    # Optionally save or display the returned image
    blended_image.show()  # Display the blended image


