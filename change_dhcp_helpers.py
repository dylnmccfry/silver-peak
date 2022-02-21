import requests
import json
import urllib3
import getpass

# Edit these variables for your environment
new_dhcp_server = '1.1.1.1'
old_dhcp_server = '10.77.52.236'
orchestrator_fqdn = 'your-orch-use1.silverpeak.cloud'





login_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/login'
logout_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/logout'

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Orchestrator admin credentials
username = input('Username: ')
password = getpass.getpass()

# List of network devices from csv
silver_peak_ids = []
with open("ids.txt") as file:
    silver_peak_ids = file.readlines()
    silver_peak_ids = [line.rstrip() for line in silver_peak_ids]

requestData = { "user": username, "password": password }

# start session
s = requests.Session()

# login
r = s.post(login_url, json=requestData, headers={'Content-Type': 'application/json'}, verify=False)

for id in silver_peak_ids:
    get_deployment_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/deployment/{id}'
    deployment_config = s.get(get_deployment_config_url, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    deployment_config = json.loads(deployment_config.text)
    for interface in deployment_config['modeIfs'][0]['applianceIPs']:
        if 'dhcpd' in interface:
            if old_dhcp_server in interface['dhcpd']['relay']['dhcpserver']:
                print(old_dhcp_server, 'has been found and replaced under this interface:', interface['ip'], 'host device:', id)
                interface['dhcpd']['relay']['dhcpserver'].remove(old_dhcp_server)
                interface['dhcpd']['relay']['dhcpserver'].append(new_dhcp_server)
    set_deployment_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/appliance/rest/{id}/deployment'
    set_deployment_config = s.post(set_deployment_config_url, json=deployment_config, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    print(set_deployment_config.text)
    print('')

# Logout of HTTP session
r = s.get(logout_url, headers={'Content-Type': 'application/json'}, verify=False)
print(r.text)
