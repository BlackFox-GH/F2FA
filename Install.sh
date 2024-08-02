#!/bin/bash

#copy the files to the opt folder
mkdir /opt/F2FA
cp server/F2FA.py /opt/F2FA/F2FA.py
if [ -f "server/F2FA.conf" ]; then
    cp server/F2FA.conf /opt/F2FA/F2FA.conf
fi

#setup python venv
python -m venv /opt/F2FA/venv

#write systemd info to file
echo "[Unit]" > /etc/systemd/system/F2FA.service
echo "Description=F2FA server" >> /etc/systemd/system/F2FA.service
echo "After=multi-user.target" >> /etc/systemd/system/F2FA.service
echo "[Service]" >> /etc/systemd/system/F2FA.service
echo "Type=simple" >> /etc/systemd/system/F2FA.service
echo "Restart=always" >> /etc/systemd/system/F2FA.service
echo "ExecStart=/opt/F2FA/venv/bin/python /opt/F2FA/F2FA.py" >> /etc/systemd/system/F2FA.service
echo "[Install]" >> /etc/systemd/system/F2FA.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/F2FA.service

#start service
systemctl daemon-reload
systemctl enable F2FA.service
systemctl start F2FA.service
