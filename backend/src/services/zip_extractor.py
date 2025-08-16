# File: backend/services/zip_extractor.py

import os, zipfile, uuid, shutil
from fastapi import UploadFile

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

def save_and_extract_zip(file: UploadFile) -> str:
    """
    Saves the uploaded file to disk and extracts it to a unique temp directory.
    Returns the extracted directory path.
    """
    # Generate a unique ID for the session
    temp_id = str(uuid.uuid4())

    # Create directory to store this upload
    upload_path = os.path.join(TEMP_DIR, temp_id)
    os.makedirs(upload_path, exist_ok=True)

    # Save file to disk
    zip_path = os.path.join(upload_path, "project.zip")
    with open(zip_path, "wb") as f:
        f.write(file.file.read())

    # Extract zip content
    extract_path = os.path.join(upload_path, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    return extract_path
