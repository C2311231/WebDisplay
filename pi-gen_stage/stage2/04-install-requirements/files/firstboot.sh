#!/bin/bash
if [ -f /etc/ld.so.preload ]; then
    rm /etc/ld.so.preload
fi

systemctl disable firstboot