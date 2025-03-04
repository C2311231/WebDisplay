#!/bin/bash -e

cp -R /WebDisplay "${ROOTFS_DIR}"
on_chroot << EOF
        pip install --break-system-packages -r /WebDisplay/requirements_cec.txt
EOF

cp files/WebDisplay.service "${ROOTFS_DIR}/etc/systemd/system"
on_chroot << EOF
        chown root:root /etc/systemd/system/WebDisplay.service
        chmod 644 /etc/systemd/system/WebDisplay.service
        systemctl enable WebDisplay
EOF

# Delete now-unnecessary custom pigen stuff.
on_chroot << EOF
        rm -rf /WebDisplay/pi-gen_stage
EOF

on_chroot << EOF
        sed -i '/SystemMaxUse/c\SystemMaxUse=10M' /etc/systemd/journald.conf
EOF
on_chroot << EOF
        chown root:root /etc/rc.local
        chmod a+x /etc/rc.local
EOF