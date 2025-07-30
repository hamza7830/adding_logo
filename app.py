import os
import zipfile
import shutil
import requests
import pandas as pd
import tempfile
from PIL import Image
from io import BytesIO
import streamlit as st
from pathlib import Path
from add_logo import add_logo_to_image

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Logo Stamper", layout="centered")
st.markdown("""
<style>
/* Fullscreen & Light Grey Background */
html, body, .block-container {
    background-color: #f2f2f2;
    padding-left: 10rem;
    padding-right: 10rem;
    padding-top: 2rem;
    padding-bottom: 2rem;

    max-width: 100% !important;
    width: 100% !important;
    max-height: 100vh;
    overflow-y: auto;
}

/* Page Padding */
.block-container {
    padding-left: 10rem;
    padding-right: 10rem;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Button Styles */
.stButton>button, .stDownloadButton>button {
    background-color: #a51c1c;
    color: white;
    font-weight: bold;
    border-radius: 5px;
    padding: 0.5em 2em;
}

/* Subheader in Red & Bold */
h3 {
    color: #a51c1c;
    font-weight: 700;
}

/* TextArea background white */
.stTextArea textarea {
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 5px !important;
}

/* FileUploader dropzone white */
div[data-testid="stFileUploader"] {
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 5px !important;
    padding: 0.5em;

}

/* Selectbox background white */
div[data-baseweb="select"] > div {
    background-color: white !important;
    border: 1px solid #ccc !important;
    border-radius: 5px !important;
}
</style>
""", unsafe_allow_html=True)


st.title("BBC Logo Stamper Tool")
# ----------------- Inputs Section -----------------
st.subheader("Upload Images or Paste URLs")
uploaded_files = st.file_uploader(
    "Upload image(s) or Excel file with image URLs",
    type=["jpg", "jpeg", "png", "xlsx"],
    accept_multiple_files=True
)
url_input = st.text_area("Paste image URLs here (one per line):")

# ----------------- Language Section -----------------
st.subheader(" Select Language ")
logo_folder = "logos"
available_languages = [
    name for name in os.listdir(logo_folder)
    if os.path.isdir(os.path.join(logo_folder, name))
]

if available_languages:
    selected_language = st.selectbox("Select Logo Language", available_languages)
else:
    st.warning("⚠️ No logo folders found in 'logos/'.")

# Construct logo path
logo_filename = f"BBC_News_Linear_{selected_language}_HR_RGB.jpg"
logo_path = f"logos/{selected_language}/Linear/Web/RGB/{logo_filename}"

# ----------------- Processing Section -----------------
st.subheader("⚙️ Process Images")

if st.button("Process Images"):
    # os.makedirs("tmp/output", exist_ok=True)
    # Always start fresh: delete and recreate output folder
    output_dir = "output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext == ".xlsx":
                # Excel file: process URLs inside
                try:
                    df = pd.read_excel(file)
                    url_column = df.columns[0]
                    csv_urls = df[url_column].dropna().tolist()
                    for idx, url in enumerate(csv_urls):
                        try:
                            response = requests.get(url)
                            response.raise_for_status()
                            img = Image.open(BytesIO(response.content))
                            # Convert to RGB if JPEG
                            original_format = img.format or "JPEG"
                            if original_format.upper() == "JPEG":
                                img = img.convert("RGB")
                            # Create temp file
                            suffix = f".{original_format.lower()}"
                            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_img:
                                img.save(tmp_img, format=original_format)
                                tmp_img_path = tmp_img.name
                            # original_format = img.format or "JPEG"
                            # ext = original_format.lower()
                            # temp_name = f"excel_url_image_{idx}.{ext}"
                            # temp_path = os.path.join("tmp/output", temp_name)

                            # if original_format.upper() == "JPEG":
                            #     img = img.convert("RGB")
                            # img.save(temp_path, format=original_format)
                            add_logo_to_image(tmp_img_path, logo_path, selected_language)
                        except Exception as e:
                            st.warning(f"Failed to process URL from Excel: {url}\nError: {e}")
                except Exception as e:
                    st.error(f"❌ Error reading Excel file: {e}")
            elif file_ext in [".jpg", ".jpeg", ".png"]:
                # Image file: save and process
                # safe_name = Path(file.name).stem
                # temp_path = os.path.join("tmp/output", f"{safe_name}{file_ext}")
                # with open(temp_path, "wb") as f:
                #     f.write(file.read())
                # Save uploaded image to a temp file, pass path to existing function
                  # Preserve original filename
                original_filename = file.name
                # Create temp folder if not already
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, original_filename)

                # Save uploaded image to temp path
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                add_logo_to_image(temp_path, logo_path, selected_language)                

            else:
                st.warning(f"Unsupported file type: {file.name}")
    # From pasted URLs
    if url_input.strip():
        urls = url_input.strip().splitlines()
        for idx, url in enumerate(urls):
            try: 
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
  # Convert to RGB if JPEG
                original_format = img.format or "JPEG"
                if original_format.upper() == "JPEG":
                    img = img.convert("RGB")
                # Create temp file
                suffix = f".{original_format.lower()}"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_img:
                    img.save(tmp_img, format=original_format)
                    tmp_img_path = tmp_img.name
                # original_format = img.format or "JPEG"
                # original_ext = original_format.lower()
                # temp_name = f"url_image_{idx}.{original_ext}"
                # temp_path = os.path.join("tmp/output", temp_name)

                # if original_format.upper() == "JPEG":
                #     img = img.convert("RGB") 
                # img.save(temp_path, format=original_format)
                add_logo_to_image(tmp_img_path, logo_path, selected_language)
            except Exception as e:
                st.warning(f"Failed to process URL {url}: {e}")

# ----------------- Download Section -----------------
st.subheader("📥 Download Processed Images")

if os.path.exists("output") and any(fname.lower().endswith((".png", ".jpg", ".jpeg")) for fname in os.listdir("output")):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for fname in os.listdir("output"):
            fpath = os.path.join("output", fname)
            if os.path.isfile(fpath):
                zip_file.write(fpath, arcname=fname)
    zip_buffer.seek(0)

    st.download_button(
        label="📦 Download All (ZIP)",
        data=zip_buffer,
        file_name="logo_stamped_images.zip",
        mime="application/zip"
    )
else:
    st.info("No processed images found yet.")
