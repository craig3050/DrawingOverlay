import streamlit as st
import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import shutil
from PIL import Image
import zipfile
from DrawingColour import PDFToImageProcessor
from DrawingOverlay import ImageOverlay
from FileNameMatcher import FileNameMatcher

# Define the base directory for processing
BASE_DIR = Path("Processing")
BASE_DIR.mkdir(exist_ok=True)

# Generate directories with UUIDs inside the Processing folder
DIR1 = BASE_DIR / f"PreviousRevision_{uuid.uuid4()}"
DIR2 = BASE_DIR / f"CurrentRevision_{uuid.uuid4()}"
OUTPUT_DIR = BASE_DIR / f"Output_{uuid.uuid4()}"
ZIP_OUTPUT_DIR = BASE_DIR / f"ZippedOutput_{uuid.uuid4()}"

# Create the directories if they don't exist
DIR1.mkdir(exist_ok=True)
DIR2.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
ZIP_OUTPUT_DIR.mkdir(exist_ok=True)

# Cleanup function
def cleanup_old_folders(base_dir, days_old=1):
    """Remove folders inside the base_dir that are older than the specified days."""
    now = datetime.now()
    cutoff_time = now - timedelta(days=days_old)

    for folder in base_dir.iterdir():
        if folder.is_dir():
            folder_mod_time = datetime.fromtimestamp(folder.stat().st_mtime)
            if folder_mod_time < cutoff_time:
                try:
                    shutil.rmtree(folder)  # Delete the folder and its contents
                    print(f"Deleted old folder: {folder}")
                except Exception as e:
                    print(f"Error deleting folder {folder}: {e}")

# Run the cleanup before continuing
cleanup_old_folders(BASE_DIR)

# Initialize session state for matches
if 'matches' not in st.session_state:
    st.session_state.matches = []

def save_files(uploaded_files, directory):
    """Save uploaded files to the specified directory with feedback."""
    if not uploaded_files:
        return

    with st.spinner("Uploading files..."):
        for uploaded_file in uploaded_files:
            file_path = directory / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"Uploaded: {uploaded_file.name}")
    st.info("All files uploaded successfully!")

def get_unique_filename(base_path, filename):
    """Generate a unique file name by appending (1), (2), etc. if the file already exists."""
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(base_path / unique_filename):
        unique_filename = f"{base}({counter}){ext}"
        counter += 1
    return unique_filename

def process_matches(matches, dir1, dir2, output_dir, color1="blue", color2="red", transparency=0.5):
    """Process the matched files and overlay images."""
    progress = st.empty()
    for i, match in enumerate(matches, 1):
        file1, file2 = match
        try:
            # Process the first file to the chosen color
            processor = PDFToImageProcessor()
            processor.set_target_color(color1)
            image1_overlay = processor.process_pdf(dir1 / file1, page_number=0)

            # Process the second file to the chosen color
            processor.set_target_color(color2)
            image2_overlay = processor.process_pdf(dir2 / file2, page_number=0)

            # Overlay images
            overlay_instance = ImageOverlay(image1_overlay, image2_overlay, transparency)
            blended_image = overlay_instance.overlay()

            # Save the blended image
            unique_filename = get_unique_filename(output_dir, f"{file2}.png")
            blended_image.save(output_dir / unique_filename)

            progress.text(f"Processed {i}/{len(matches)}: {file1} and {file2}")
        except Exception as e:
            progress.text(f"Error processing {file1} and {file2}: {e}")
    st.success("All matches processed successfully!")

def create_zip_file(output_dir, zip_output_dir):
    """Create a ZIP file of all files in the output directory in a separate directory."""
    zip_path = zip_output_dir / "output_files.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in output_dir.iterdir():
            if file.is_file():
                zipf.write(file, arcname=file.name)
    return zip_path

# Streamlit app layout with full-width mode
st.set_page_config(layout="wide")

# Add a custom header
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 20px; background-color: #f4f4f4;">
        <div style="display: flex; align-items: center;">
            <img src="https://cuninghamedesign.co.uk/wp-content/uploads/2025/01/logo-1.webp?w=71&h=71" alt="Logo" style="height: 50px; margin-right: 15px;">
            <h1 style="margin: 0; font-size: 1.5rem;">Cuninghame Design Ltd</h1>
        </div>
        <div>
            <a href="https://www.cuninghamedesign.co.uk" target="_blank" style="text-decoration: none; color: #007bff; font-size: 1rem;">Visit our Website</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Layout Revision Comparison App")

# Define columns with custom widths
col1, col2, col3 = st.columns([1, 1, 2])  # Column 3 is twice as wide as columns 1 and 2

# Left-hand file uploader and color selector
with col1:
    st.header("Upload Previous Revision")
    uploaded_files_dir1 = st.file_uploader("Drag files here", accept_multiple_files=True, key="uploader_dir1")
    color1 = st.selectbox("Select color for Previous Revision:", ["Blue", "Red", "Green", "Orange", "Pink", "Yellow"]).lower()
    if uploaded_files_dir1:
        save_files(uploaded_files_dir1, DIR1)

# Right-hand file uploader and color selector
with col2:
    st.header("Upload Current Revision")
    uploaded_files_dir2 = st.file_uploader("Drag files here", accept_multiple_files=True, key="uploader_dir2")
    color2 = st.selectbox("Select color for Current Revision:", ["Red", "Blue", "Green", "Orange", "Pink", "Yellow"]).lower()
    if uploaded_files_dir2:
        save_files(uploaded_files_dir2, DIR2)

# Match files and display results
with col3:
    st.header("File Processing")
    sample_file_name = st.text_input(
        "Enter a sample file name [used to match variations in file names (e.g., revision numbers)]:"
    )

    if st.button("1) Match Files"):
        if sample_file_name:
            matcher = FileNameMatcher(DIR1, DIR2, sample_file_name)
            st.session_state.matches = matcher.find_matches()
            st.write(f"Number of matches: {len(st.session_state.matches)}")
            match_display = "\n".join([f"{m[0]} == {m[1]}" for m in st.session_state.matches]) if st.session_state.matches else "No matches found."
            st.text_area("Matches", match_display, height=200)
        else:
            st.warning("Please enter a sample file name.")

    if st.session_state.matches:
        if st.button("2) Process Matches"):
            process_matches(st.session_state.matches, DIR1, DIR2, OUTPUT_DIR, color1, color2)
            zip_path = create_zip_file(OUTPUT_DIR, ZIP_OUTPUT_DIR)
            st.download_button(
                label="3) Download Processed Files",
                data=open(zip_path, "rb").read(),
                file_name="output_files.zip",
                mime="application/zip"
            )
