#!/bin/bash

# Set X environment variables
export XAUTHORITY="$HOME/.Xauthority"
export DISPLAY=:0
sleep 2
# Disable screen blanking and power management
xset s off
xset s noblank
xset -dpms

# Start Openbox
unclutter -idle 2 &
exec openbox-session