import requests
import json
import urllib3
import getpass

# Edit these variables for your environment
new_dhcp_servers = ['1.1.1.1', '2.2.2.2', '3.3.3.3']
orchestrator_fqdn = 'your-orch-use1.silverpeak.cloud'

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

login_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/login'
logout_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/logout'

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
            if 'relay' in interface['dhcpd']:
                print('Replacing DHCP relays...')
                interface['dhcpd']['relay']['dhcpserver'].clear()
                interface['dhcpd']['relay']['dhcpserver'].extend(new_dhcp_servers)
    set_deployment_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/appliance/rest/{id}/deployment'
    set_deployment_config = s.post(set_deployment_config_url, json=deployment_config, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    print(set_deployment_config.text)
    print('')

# Logout of HTTP session
r = s.get(logout_url, headers={'Content-Type': 'application/json'}, verify=False)
print(r.text)
