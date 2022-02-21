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
get_all_appliances = f'https://{orchestrator_fqdn}:443/gms/rest/appliance'
all_appliances = s.get(get_all_appliances, verify=False, headers = {'Content-Type': 'application/json'}, cookies=r.cookies)
all_appliances = json.loads(all_appliances.text)

f = open("output.csv", "w")

# Create and write to csv file with hostname and network ID

for appliance in all_appliances:
    f.write(appliance['hostName'] + ',' + appliance['id'])
    f.write("\n")
f.close()
# Logout of HTTP session
r = s.get(logout_url, headers={'Content-Type': 'application/json'}, verify=False)
print(r.text)
