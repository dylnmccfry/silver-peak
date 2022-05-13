import requests
import json
import urllib3
import getpass
import time

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Orchestrator FQDN
orchestrator_url = 'yourcloud.cloud.com'
# read/write API key
api_key = input('API KEY: ')
# ID of Silver Peak device
device_id = input('Device ID: ')
# Interface to shut/no shut
interface = input('Interface: ')

# Shutdown interface specified section
dhcp_command = ['interface', interface, 'shutdown']
my_dict = {'neList': [device_id], 'cmdList': [" ".join(dhcp_command)] }
data = json.dumps(my_dict, indent = 4)
print('Shutting down', interface)
broadcast_url = f'https://{orchestrator_url}:443/gms/rest/broadcastCli/?apiKey={api_key}'
response = requests.request('POST', broadcast_url, headers = {'Content-Type': 'application/json'}, data = data, verify=False)
print(response.status_code)

print('Pausing for 5 seconds to allow Orchestrator to execute change...')
time.sleep(5)

# No shut interface specified section
print('Turning up interface', interface)
dhcp_command = ['no', 'interface', interface, 'shutdown']
my_dict = {'neList': [device_id], 'cmdList': [" ".join(dhcp_command)] }
data = json.dumps(my_dict, indent = 4)
broadcast_url = f'https://{orchestrator_url}:443/gms/rest/broadcastCli/?apiKey={api_key}'
response = requests.request('POST', broadcast_url, headers = {'Content-Type': 'application/json'}, data = data, verify=False)
print(response.status_code)
