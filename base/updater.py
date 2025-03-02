import os
import shutil
import zipfile
import requests
import sys


CURRENT_VERSION_FILE = "version.txt"
VERSION_URL = 'https://raw.githubusercontent.com/C2311231/WebDisplay/main/version.txt'
UPDATE_ZIP_URL = 'https://github.com/C2311231/WebDisplay/releases/latest/download/release.zip'
STAGING_DIR = 'staging'

def read_current_version():
    try:
        with open(CURRENT_VERSION_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"  # Assume very old version if missing

def get_latest_version():
    response = requests.get(VERSION_URL)
    response.raise_for_status()
    return response.text.strip()

def download_and_extract_update():
    os.makedirs(STAGING_DIR, exist_ok=True)
    zip_path = os.path.join(STAGING_DIR, 'update.zip')

    response = requests.get(UPDATE_ZIP_URL, stream=True)
    response.raise_for_status()
    with open(zip_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(STAGING_DIR)

    os.remove(zip_path)

def apply_update():
    # Move files from staging to app directory
    for item in os.listdir(STAGING_DIR):
        source = os.path.join(STAGING_DIR, item)
        destination = os.path.join(".", item)

        if os.path.exists(destination):
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            else:
                os.remove(destination)

        shutil.move(source, destination)

    shutil.rmtree(STAGING_DIR)

def restart_app():
    """Cross-platform app restart"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

def check_for_updates():
    try:
        latest_version = get_latest_version()
        if latest_version > read_current_version():
            return {'update_available': True, 'latest_version': latest_version}
        else:
            return {'update_available': False, 'latest_version': read_current_version()}
    except Exception as e:
        return {'error': str(e)}

def perform_update():
    try:
        download_and_extract_update()
        apply_update()
        return {'status': 'update_applied'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}