import requests
import json
import urllib3
import getpass
# Silence the insecure warning due to SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

orchestrator_fqdn = 'your-orch-use1.silverpeak.cloud'

# Orchestrator admin credentials
username = input('Username: ')
password = getpass.getpass()

# Cloud hosted orchestrator URL

login_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/login'
logout_url = f'https://{orchestrator_fqdn}:443/gms/rest/authentication/logout'
# Username and password dictionary
requestData = { "user": username, "password": password }

# start session
s = requests.Session()

# login with credentials to get session cookie for remaining API calls
r = s.post(login_url, json=requestData, headers={'Content-Type': 'application/json'}, verify=False)
#Gets all appliance information, to be used to grab the Hostname and ID
print('Connecting to API...')
get_all_appliances = f'https://{orchestrator_fqdn}:443/gms/rest/appliance'
all_appliances = s.get(get_all_appliances, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
all_appliances = json.loads(all_appliances.text)
print('Creating csv file...')
f = open("output.csv", "w")
f.write('Hostname' + ',' + 'ID' + ',' + 'Loopback IP')
f.write("\n")
f.close()
f = open("output.csv", "a")
print('Getting loopback IP, hostname, and ID of each appliance and writing to csv...')
#Iterates through each appliance to create csv
for appliance in all_appliances:
    id = appliance['id']
    get_loopback_config_url = f'https://{orchestrator_fqdn}:443/gms/rest/virtualif/loopback/{id}?cached=true'
    loopback_ip = s.get(get_loopback_config_url, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
    loopback_ip = json.loads(loopback_ip.text)
    try:
        loopback_ip = loopback_ip[(list(loopback_ip.keys())[0])]
        f.write(appliance['hostName'] + ',' + appliance['id'] + ',' + loopback_ip['ipaddr'])
        f.write("\n")

    except IndexError:
        print(appliance['hostName'], 'Does not have a loopback interface...Skipping')
f.close()
# Logout of HTTP session
r = s.get(logout_url, headers={'Content-Type': 'application/json'}, verify=False)
print(r.text)
