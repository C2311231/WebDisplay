#!/bin/bash
xset -dpms
xset s off
xset s noblank
exec openbox-session
exec unclutter -idle 1 &