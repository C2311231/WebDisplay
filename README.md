
# WebDisplay
> **Work in progress**

Simple project to remotely manage and control a web browser for digital signage
#### Features
- Display Google Slides
- Display Websites
- Event Scheduling
- CEC Support (Control Screen Power)
- Live Screenshots
- Easy Updating
- Easy Multi-device Management
- Multi-device Events
- Premade Raspberry Pi Image
#### Upcoming Features
- Multiple Display Support
- Networking Configuration
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

#### Raspberry PI Install
1. Download and install Raspberry Pi Imager: https://www.raspberrypi.com/software/
1. Download the image artifact from the most recent successful build: https://github.com/C2311231/WebDisplay/actions/workflows/main.yml
1. Run Raspberry Pi Imager and select the desired device, then chose custom image then select the downloaded image, then pick your desired storage device and click next.
1. It should provide the option to configure user information and wifi, if you are using wifi you can configure it here, and change the default password if you would like (Username may not be changed).
1. Flash the micro sd card and install it into the RPI.
1. Boot the RPI, and it should automatically complete the rest of the setup after a few minutes.
1. It should now be accessible at http://{device ip}:5000.
#### Windows Install (Coming Soon)
### Usage
#### Running Manually:
    /{path/to/WebDisplay/directory}/.venv/bin/python3 /{path/to/WebDisplay/directory}/main.py db.db {port}
#### Accessing the Web Interface:
The web interface is available at: http://{device ip}:{port}  
Other devices should automatically be detected and added to the side menu.

## To Do
- Add multi display (per device) support
- Add user defined templates
- Add automated tests
- Improved UI
    - Tooltips / Setting Descriptions
    - Centralized management
        - Global On/Off
        - Group Managment
    - Add networking config
    - Improved event scheduling
        - Event Priorities
        - Device Groups (Device can be a member of multiple groups)
        - algorithmic Scheduling
        - Day Specific overrides (For holidays or other events)
        - Percentage Based Event Deployment with dynamic reallocation (20% show one event 80% another...)
- Create Install Script
- Improved device onboarding
    - Bluetooth adoption
    - WiFi hotspot
    - Onboarding Screen with instructions
- Video Events
    - Transcode to optimal res/codec (h265 up to 4k rpi 5, h264 1080 for rest)
    - Synchronous video events (Multiple devices in near frame perfect sync)
    - Audio sync
    - Video streams (RTMP, WebRTC)