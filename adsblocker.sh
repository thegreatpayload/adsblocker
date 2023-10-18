#!/bin/bash

echo "...Start..."
apt-get update
apt-get upgrade -y

echo "....Installing Bind9...."
#Installing Bind9 (DNS Server)
apt-get install -y bind9

echo "....Copying Configuration Fles..."
cp named.conf /etc/bind/named.conf
cp adsblocker.py /etc/bind/adsblocker.py

echo "....Fetch updated domain list..."
python3 adsblocker.py

echo "...Restart Services..."
systemctl restart named
systemctl restart bind9

echo "...Verify Data..."
named-checkconf
named-checkconf rpz /etc/bind/adsblocker.db

#Schedule Cron Job to fetch updated domain list
echo "...set Cronjob for future update..."
crontab -l > adsblocker
#cron job which will run at 00:00 on Sunday.
echo "0 0 * * 0 sudo python3 /etc/bind/adsblocker.py>> /etc/bnd/adsblocker.log" >> adsblocker
#install new cron file
crontab adblocker

rm adsblocker
echo "...Finish... "