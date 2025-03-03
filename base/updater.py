import os
import shutil
<<<<<<< HEAD
import subprocess
import datetime
import requests


# Configuration
REPO_URL = 'https://github.com/C2311231/WebDisplay.git'
LOCAL_DIR = './'
ARCHIVE_DIR = '../archives'
BRANCH = 'main'


def fetch_readme_from_github():
    url = "https://raw.githubusercontent.com/C2311231/WebDisplay/main/README.md"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch README.md (status code {response.status_code})"


def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stderr)
        exit(1)
        
def get_local_commit():
    """Gets the current local commit hash."""
    result = subprocess.run('git rev-parse HEAD', shell=True, cwd=LOCAL_DIR, capture_output=True, text=True)
    return result.stdout.strip()

def get_remote_commit():
    """Fetches the latest commit hash from the remote branch."""
    run_command('git fetch', cwd=LOCAL_DIR)  # Fetch latest data
    result = subprocess.run(f'git rev-parse origin/{BRANCH}', shell=True, cwd=LOCAL_DIR, capture_output=True, text=True)
    return result.stdout.strip()

def is_update_available():
    """Check if local and remote commits differ."""
    if not os.path.exists(LOCAL_DIR):
        # If there's no local repo, we need an update (initial clone)
        return True

    local_commit = get_local_commit()
    remote_commit = get_remote_commit()

    print(f"Local commit:  {local_commit}")
    print(f"Remote commit: {remote_commit}")

    return local_commit != remote_commit


def should_skip(path):
    """ Return True if the folder should be skipped (starts with .) """
    print(os.path.basename(path))
    return os.path.basename(path).startswith('.')

def copy_tree_filtered(src, dst):
    """ Copy src to dst, skipping directories starting with '.' """
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src):
        # Skip directories starting with '.'
        dirs[:] = [d for d in dirs if not should_skip(d)]

        # Relative path from src root
        rel_path = os.path.relpath(root, src)
        target_root = os.path.join(dst, rel_path)

        # Make sure target directory exists
        os.makedirs(target_root, exist_ok=True)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_root, file)
            shutil.copy2(src_file, dst_file)

def archive_current_version():
    if not os.path.exists(LOCAL_DIR):
        print(f"No existing '{LOCAL_DIR}' directory to archive.")
        return

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    archive_path = os.path.join(ARCHIVE_DIR, f'backup-{timestamp}')

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    print(f"Archiving to {archive_path}, skipping hidden directories.")
    copy_tree_filtered(LOCAL_DIR, archive_path)
    
def clone_or_update_repo():
    if os.path.exists(LOCAL_DIR):
        print(f"Updating existing repository in {LOCAL_DIR}")
        run_command(f'git fetch', cwd=LOCAL_DIR)
        run_command(f'git reset --hard origin/{BRANCH}', cwd=LOCAL_DIR)
    else:
        print(f"Cloning repository into {LOCAL_DIR}")
        run_command(f'git clone --branch {BRANCH} {REPO_URL} {LOCAL_DIR}')

def main():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # Archive the current version (skip hidden directories like .git and .venv)
    archive_current_version()

    # Clone or update the repository
    clone_or_update_repo()

    print("Update complete.")

if __name__ == '__main__':
    main()