import requests
import json
import urllib3
import getpass
import ipaddress
import csv


#Edit these variables for your environment
new_dhcp_servers = ['1.1.1.1', '9.9.9.9']
orchestrator_fqdn = 'your-orch-use1.silverpeak.cloud'
# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Orchestrator admin credentials
username = input('Username: ')
password = getpass.getpass()

# List of network devices from csv
silver_peak_ids = []
silver_peak_subnets = []
with open("ids.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        silver_peak_ids.append(row[0])
        silver_peak_subnets.append(row[1])
        #print(silver_peak_ids)
        #print(silver_peak_subnets)


login_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/login'
logout_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/logout'

requestData = { "user": username, "password": password }

# start session
s = requests.Session()

# login
r = s.post(login_url, json=requestData, headers={'Content-Type': 'application/json'}, verify=False)

for id, subnet in zip(silver_peak_ids, silver_peak_subnets):
    get_deployment_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/deployment/{id}'
    deployment_config = s.get(get_deployment_config_url, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    deployment_config = json.loads(deployment_config.text)
    print('PRECHANGE DEPLOYMENT CONFIG',deployment_config)
#Debugging to print deployment config to compare it before any changes
    for interface in deployment_config['modeIfs'][0]['applianceIPs']:
        interface_ip = str(interface['ip'])
        if 'dhcpd' in interface and ipaddress.ip_address(interface_ip) in ipaddress.ip_network(subnet):
            print('This has an interface in the specified subnet and would change', interface['ip'])
            if 'relay' in interface['dhcpd']:
                print('Replacing DHCP relays...')
                interface['dhcpd']['relay']['dhcpserver'].clear()
                interface['dhcpd']['relay']['dhcpserver'].extend(new_dhcp_servers)
#Debugging to print the deployment config after changes
                print('POST CHANGE DEPLOYMENT CONFIG',deployment_config)
                break
        else:
            print('This interface is not in the same subnet as:',interface_ip,'Subnet:',subnet,'or is not setup for dhcp relay' )
            print('No deployment changes have been made.')
            print(deployment_config)
    set_deployment_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/appliance/rest/{id}/deployment'
    set_deployment_config = s.post(set_deployment_config_url, json=deployment_config, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    print(set_deployment_config.text)
    print('')

#config_file = open("deployment_config.json", "w")
#config_file.write(str(deployment_config))
#config_file.close
