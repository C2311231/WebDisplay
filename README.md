
# WebDisplay
> **Work in progress (Not ready for production)**

Simple project to remotely manage and control a web browser for digital signage
#### Features
- Display Google Slides
- Display Websites
- Event Scheduling
- CEC Support (Control Screen Power)
- Live Screenshots
- Easy Updating
- Easy Multi-device Managment
- Multi-device Events
- Premade Raspberry Pi Image
#### Upcoming Features
- Multiple Display Support
- Networking Configuration
- ICS Calender Support
- User Defined Templates

## Documentation

### Getting Started
#### Debian Based Install

Install dependencies:

    sudo apt update
    sudo apt install -y chromium-chromedriver chromium python3 python3-pip unclutter git ## Also install libcec-dev if cec is supported

Create required directories and create and pull git repository:

    mkdir archives
    mkdir WebDisplay
    cd WebDisplay
    git init
    git remote add origin https://github.com/C2311231/WebDisplay.git
    git pull origin main

Create virtual env and install python requirements

    python -m venv .venv
    source .venv/bin/activate
    pip install --break-system-packages -r requirements.txt ## If using CEC replace "requirements.txt" with "requirements_cec.txt"
    deactivate

#### (Optional) Run on boot
Create system service

    sudo nano /etc/systemd/system/WebDisplay.service

Paste this config (Fill in placeholders {})

    [Unit]
    Description=WebDisplay Service

    [Install]
    WantedBy=default.target

    [Service]
    User={Username}
    Restart=always
    ExecStart=/{path/to/WebDisplay/directory}/.venv/bin/python3 /{path/to/WebDisplay/directory}/main.py db.db {port}
    WorkingDirectory=/{path/to/WebDisplay/directory}

Enable Service

    sudo systemctl enable WebDisplay

#### Windows Install (Coming Soon)
### Usage
#### Running Manualy:
    /{path/to/WebDisplay/directory}/.venv/bin/python3 /{path/to/WebDisplay/directory}/main.py db.db {port}
#### Accessing the Web Interface:
The web interface is available at: http://{device ip}:{port}  
Other devices should automatically be detected and added to the side menu.

























## To Do
- Add multi display support
- Document
- Improve Error Handling
- Add user defined templates
- Add automated tests
- Add ICS calender support
- Add networking config