#!/bin/bash -e

cp -R ../../WebDisplay "${ROOTFS_DIR}"
on_chroot << EOF
        useradd webdisplay
        chmod 755 /WebDisplay/
        python -m venv /WebDisplay/.venv
        source /WebDisplay/.venv/bin/activate
        pip install --break-system-packages -r /WebDisplay/requirements_cec.txt
        deactivate
EOF

cp files/WebDisplay.service "${ROOTFS_DIR}/etc/systemd/system"
cp files/startx@.service "${ROOTFS_DIR}/etc/systemd/system"
cp files/Xwrapper.config "${ROOTFS_DIR}/etc/X11/Xwrapper.config"
cp files/.xinitrc "${ROOTFS_DIR}/home/pi/.xinitrc"
on_chroot << EOF
        chown root:root /etc/systemd/system/WebDisplay.service
        chmod 644 /etc/systemd/system/WebDisplay.service
        chmod 777 /home/pi/.xinitrc
        systemctl enable WebDisplay

        chown root:root /etc/systemd/system/startx@.service
        chmod 644 /etc/systemd/system/startx@.service
        systemctl enable startx@pi
EOF


# Delete now-unnecessary custom pi-gen stuff.
on_chroot << EOF
        rm -rf /WebDisplay/pi-gen_stage
EOF

on_chroot << EOF
        sed -i '/SystemMaxUse/c\SystemMaxUse=10M' /etc/systemd/journald.conf
EOF