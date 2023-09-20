import requests
import json

# Cloudflare API credentials
token = open('cf', 'r').read()
url = "https://api.cloudflare.com/client/v4/zones/cdafb8e2fe2bf800169cfd31109e8b74/dns_records/987df81d1510ab214a7c4fe289b3bb91"
headers = {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
# Function to get your current public IP address
def get_ip():
    try:
        r = requests.get('http://ipv4.icanhazip.com')
        if (r.status_code == 200):
            return r.text.strip()
    except Exception as e:
            print("An error occuured while fetching your IP:", e)

# get current DNS Record
def get_record():
    try:
        current_ip = json.loads(requests.get(url,headers=headers).text)["result"]["content"]
        return current_ip
    except Exception as e:
         print("Couldn't get the current DNS record", e)

# Update URL if it differs
def update_ip(cip):
    data = json.dumps({'content':f"{cip}",'name':'home.mort.cc','type':'A'})    
    try:
        submit_ip = requests.put(url, headers=headers, data=data,)
        if (submit_ip.status_code != 200):
            print(f"there was an error updating the IP: {submit_ip.content}")
    except Exception as e:
        print("Couldn't update the record", e)

# Code Logic
ip = get_ip()
current_ip = get_record()
if (ip == current_ip):
    print("Nothing to do; record hasn't changed")
else:
    update_ip(ip)
    print("IP Address Updated")