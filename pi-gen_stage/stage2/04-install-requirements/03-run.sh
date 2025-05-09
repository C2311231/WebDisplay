#!/bin/bash -e

cp -R ../../WebDisplay "${ROOTFS_DIR}"
on_chroot << EOF
        chmod 755 /WebDisplay/
        python -m venv /WebDisplay/.venv
        source /WebDisplay/.venv/bin/activate
        pip install --break-system-packages -r /WebDisplay/requirements_cec.txt
        deactivate
EOF

cp files/WebDisplay.service "${ROOTFS_DIR}/etc/systemd/system"
cp files/Xwrapper.config "${ROOTFS_DIR}/etc/X11/Xwrapper.config"
cp files/.xprofile "${ROOTFS_DIR}/home/pi/.xprofile"
cp files/firstboot.sh "${ROOTFS_DIR}/usr/local/sbin/firstboot.sh"
cp files/lightdm.conf "${ROOTFS_DIR}/etc/lightdm/lightdm.conf"
cp files/firstboot.service "${ROOTFS_DIR}/etc/systemd/system"
on_chroot << EOF
        chown root:root /etc/systemd/system/WebDisplay.service
        chmod 644 /etc/systemd/system/WebDisplay.service
        chmod 777 /home/pi/.xprofile
        systemctl enable WebDisplay

        chown root:root /etc/systemd/system/firstboot.service
        chmod 644 /etc/systemd/system/firstboot.service
        chmod +x /usr/local/sbin/firstboot.sh
        systemctl enable firstboot

        mkdir /archives
        chown -R pi:pi /archives/
        cd /WebDisplay
        git init --shared=0777
        git remote add origin https://github.com/C2311231/WebDisplay.git
        chown -R pi:pi /WebDisplay/
EOF

on_chroot << EOF
        sudo ln -s /etc/sv/lightdm /var/service
        sudo systemctl enable lightdm
        sed -i '/SystemMaxUse/c\SystemMaxUse=10M' /etc/systemd/journald.conf
        sudo systemctl set-default graphical.target
EOF