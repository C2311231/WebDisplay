#!/bin/bash -e

cp -R ../../WebDisplay "${ROOTFS_DIR}"
on_chroot << EOF
        python -m venv /WebDisplay/.venv
        source /WebDisplay/.venv/bin/activate
        pip install --break-system-packages -r /WebDisplay/requirements_cec.txt
        deactivate
EOF

cp files/WebDisplay.service "${ROOTFS_DIR}/etc/systemd/system"
cp files/xorg.service "${ROOTFS_DIR}/etc/systemd/system"
cp files/.xinitrc "${ROOTFS_DIR}/home/web/.xinitrc"
on_chroot << EOF
        chown root:root /etc/systemd/system/WebDisplay.service
        chmod 644 /etc/systemd/system/WebDisplay.service
        systemctl enable WebDisplay

        chown root:root /etc/systemd/system/xorg.service
        chmod 644 /etc/systemd/system/xorg.service
        systemctl enable xorg
        
        mkdir /home/web/WebDisplay/
EOF

# Delete now-unnecessary custom pi-gen stuff.
on_chroot << EOF
        rm -rf /WebDisplay/pi-gen_stage
EOF

on_chroot << EOF
        sed -i '/SystemMaxUse/c\SystemMaxUse=10M' /etc/systemd/journald.conf
        rm /etc/ld.so.preload
EOF