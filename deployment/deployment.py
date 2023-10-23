import requests
import json
import urllib3
import getpass
import csv


# Edit these variables for your environment
orchestrator_fqdn = 'your-orch.silverpeak.cloud'
deployment_backup_file = open('deployment_config_backup.json', 'w')

# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Orchestrator admin credentials
username = input('Username: ')
password = getpass.getpass()

# Which Appliance to run against
appliance_id = input('Appliance ID:')

headers = {
    'accept': '*/*',
}

params = {
    'source': 'menu_rest_apis_id',
}

login_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/login'
logout_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/logout'

requestData = { "user": username, "password": password }

# start session
s = requests.Session()

# login
r = s.post(login_url, json=requestData, headers={'Content-Type': 'application/json'}, verify=False)

# Take backup of deployment config in case of restore
get_deployment_config_url = f'https://{orchestrator_fqdn}/gms/rest/deployment/{appliance_id}'
deployment_config = s.get(get_deployment_config_url, verify=False, headers = headers, cookies=r.cookies)

config_backup = deployment_config.json()
with open('deployment_config_backup.json', 'w') as f:
    json.dump(config_backup, f, indent=4)

new_json_data = config_backup
# For loop to iterate through each IP in the CSV file and append the JSON data with IP

with open('deployment_ips.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        label = row[0] # Label used on the interface, column 1
        ip = row[1] # IP address for silver peak, column 2
        mask = row[2] # Subnet mask in slash notation, column 3
        vlan = row[3] # VLAN ID, column 4
        if row[4] == ('y' or 'Y'): # Check if relay bool is yes, Column 5
            relay = 'relay'
            dhcp1 = row[5]
            dhcp2 = row[6]
        else:
            relay = 'none' # Check if relay bool is no, Column 5
            dhcp1 = None
            dhcp2 = None
# JSON data template to append information from CSV file into memory
        new_ip = {

                    "ip": ip,
                    "mask": mask,
                    "wanNexthop": "0.0.0.0",
                    "dhcp": False,
                    "lanSide": True,
                    "wanSide": False,
                    "label": "5",
                    "harden": 0,
                    "behindNAT": "none",
                    "maxBW": {},
                    "zone": 0,
                    "comment": "",
                    "vrf": 0,
                    "vlan": vlan,
                    "dhcpd": {
                        "type": relay,
                        "server": {
                            "prefix": "0.0.0.0/0",
                            "ipStart": "0.0.0.0",
                            "ipEnd": "0.0.0.0",
                            "gw": [],
                            "dns": [],
                            "ntpd": [],
                            "netbios": [],
                            "netbiosNodeType": "B",
                            "maxLease": 0,
                            "defaultLease": 0,
                            "ip_range": {},
                            "options": {},
                            "host": {},
                            "failover": False
                        },
                        "relay": {
                            "dhcpserver": [
                                dhcp1,
                                dhcp2
                            ],
                            "option82": False,
                            "option82_policy": "append"
                        }
                    }
}
        new_json_data['modeIfs'][0]['applianceIPs'].append(new_ip)


# Pushes deployment config to appliance which includes all new values from CSV
print('Configuring Deployment config.')
set_deployment_config_url = f'https://{orchestrator_fqdn}/gms/rest/appliance/rest/{appliance_id}/deployment'
set_deployment_config = s.post(set_deployment_config_url, json=new_json_data, verify=False, headers={'Content-Type': 'application/json'}, cookies=r.cookies)
print(set_deployment_config.text)
print(set_deployment_config.status_code)

# Empties json variable to be reused for the VRRP section below
new_json_data = []
print('Configuring VRRP')
# VRRP Section, gather group ID, VIP, and interface from CSV file append json variable
with open('vrrp.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        group_id = int(row[0]) # VRRP group ID in csv
        vip = row[1] # IP address for VRRP VIP in csv
        interface = row[2] # Physical interface of silver peak

        vrrp_data = {
            "pkt_trace":False,
            "adv_timer":1,
            "preempt":True,
            "holddown":10,
            "groupId":group_id,
            "auth":"",
            "desc":"",
            "enable":"Up",
            "priority":128,
            "vipaddr":vip,
            "interface":interface,
            "mode":"",
            "master_transitions":"",
            "masterip":"",
            "uptime":"",
            "vipowner":False,
            "vmac":""
            }

        new_json_data.append(vrrp_data)
# Set URL for VRRP http post, pushes VRRP config to appliance
set_vrrp_config_url = f'https://{orchestrator_fqdn}/gms/rest/appliance/rest/{appliance_id}/vrrp'
set_vrrp_config = s.post(set_vrrp_config_url, json=new_json_data, verify=False, headers={'Content-Type': 'application/json'}, cookies=r.cookies)
print(set_vrrp_config.text)
print(set_vrrp_config.status_code)
# Logout of HTTP session
r = s.get(logout_url, json=requestData, headers= headers, verify=False)
print(r.text)
