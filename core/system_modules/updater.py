import os
import shutil
import subprocess
import datetime
import requests
import core.module
import core.system
# Configuration

REPO_URL = 'https://github.com/C2311231/WebDisplay.git'
CONTENT_URL = 'https://raw.githubusercontent.com/C2311231/WebDisplay'
LOCAL_DIR = './'
ARCHIVE_DIR = '../archives'
BRANCH = 'main'

class UpdateManager(core.module.module):
    """Class to manage updates for the WebDisplay application."""
    
    def __init__(self, system: core.system.system, repo_url: str = REPO_URL, content_url: str = CONTENT_URL,  local_dir: str = LOCAL_DIR, archive_dir:str = ARCHIVE_DIR, branch: str = BRANCH):
        self.system = system
        system.require_modules("api_registry")
        self.repo_url = repo_url
        self.local_dir = local_dir
        self.archive_dir = archive_dir
        self.branch = branch
        self.content_url = content_url
        
    def start(self):
        self.api_registar: core.api.api_register = self.system.get_module("api_registry")  # type: ignore
        return super().start()
    
    def shutdown(self):
        return super().shutdown()
    
    def update(self, delta_time: float):
        return super().update(delta_time)

    def fetch_release_notes_from_github(self):
        url = f"{self.content_url}/{self.branch}/release_notes.txt"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch release_notes.txt (status code {response.status_code})"

    def fetch_next_version_from_github(self):
        url = f"{self.content_url}/{self.branch}/version.txt"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch version.txt (status code {response.status_code})"


    def run_command(self, cmd, cwd=None):
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(result.stderr)
            exit(1)
            
    def get_local_commit(self):
        """Gets the current local commit hash."""
        result = subprocess.run('git rev-parse HEAD', shell=True, cwd=self.local_dir, capture_output=True, text=True)
        return result.stdout.strip()

    def get_remote_commit(self):
        """Fetches the latest commit hash from the remote branch."""
        self.run_command('git fetch', cwd=self.local_dir)  # Fetch latest data
        result = subprocess.run(f'git rev-parse origin/{self.branch}', shell=True, cwd=self.local_dir, capture_output=True, text=True)
        return result.stdout.strip()

    def is_update_available(self):
        """Check if local and remote commits differ."""
        if not os.path.exists(self.local_dir):
            # If there's no local repo, we need an update (initial clone)
            return True

        local_commit = self.get_local_commit()
        remote_commit = self.get_remote_commit()

        print(f"Local commit:  {local_commit}")
        print(f"Remote commit: {remote_commit}")

        return local_commit != remote_commit


    def should_skip(self, path):
        """ Return True if the folder should be skipped (starts with .) """
        print(os.path.basename(path))
        return os.path.basename(path).startswith('.')

    def copy_tree_filtered(self, src, dst):
        """ Copy src to dst, skipping directories starting with '.' """
        os.makedirs(dst, exist_ok=True)
        for root, dirs, files in os.walk(src):
            # Skip directories starting with '.'
            dirs[:] = [d for d in dirs if not self.should_skip(d)]

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

    def archive_current_version(self):
        if not os.path.exists(self.local_dir):
            print(f"No existing '{self.local_dir}' directory to archive.")
            return

        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        archive_path = os.path.join(self.archive_dir, f'backup-{timestamp}')

        os.makedirs(self.archive_dir, exist_ok=True)

        print(f"Archiving to {archive_path}, skipping hidden directories.")
        self.copy_tree_filtered(self.local_dir, archive_path)
        
    def clone_or_update_repo(self):
        if os.path.exists(self.local_dir):
            print(f"Updating existing repository in {self.local_dir}")
            self.run_command(f'git fetch', cwd=self.local_dir)
            self.run_command(f'git reset --hard origin/{self.branch}', cwd=self.local_dir)
        else:
            print(f"Cloning repository into {self.local_dir}")
            self.run_command(f'git clone --branch {self.branch} {self.repo_url} {self.local_dir}')

    def run_update(self):
        # Archive the current version (skip hidden directories like .git and .venv)
        self.archive_current_version()

        # Clone or update the repository
        self.clone_or_update_repo()

        print("Update complete.")
        exit(0)
        
    def register_api_endpoints(self) -> None:
        self.api_registar.register_endpoint("updater", 1, "update", self.run_update, "Updates to the latest version")

def register(system_manager):
    return "updater", UpdateManager(system_manager)
        
# if __name__ == '__main__':
#     updater = UpdateManager()
#     updater.run_update()