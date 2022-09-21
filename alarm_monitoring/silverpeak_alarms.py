# Used for REST api calls
import requests
# Used for formatting data for REST api
import json
# Used to read Appliance and interface to look for alarms
import csv
# Used to format EPOCH time to human readable
import datetime
# Used for converting current time to EPOCH time
import time

network_ids = []
interfaces = []
#ID of alert - An IP SLA monitor is in the Down state
alarm_id = 262189
orchestrator_url = 'https://yourorchestrator.domain/gms/rest'
url_path = '/authentication/login'
logout_url = f'{orchestrator_url}/authentication/logout'
s = requests.Session()

# Collect username and password to auth for session cookie
username = 'username'
password = 'password'
# Format username and password into json format
data = { 'user': username, 'password': password }
headers = { 'Content-type': 'application/json' }


# Login using username and password to generate cookie used for API calls
url = orchestrator_url + url_path
auth = s.post(url, json=data, headers=headers)

with open('silverpeaks.csv', 'r') as f:
	csv_reader=csv.reader(f,delimiter=',')
	for line in csv_reader:
		network_ids.append(line[0])
		interfaces.append(line[1])

# Get alarms from each Network ID
# url_path = '/alarm/appliance?severity=warning&view=active'
# Convert time from last 24 hours to epoch
yesterday = int(time.time() * 1000) - 86400000
url_path = f'/alarm/appliance?severity=warning&from={yesterday}'
url = orchestrator_url + url_path
body = {"ids":network_ids}
data = json.dumps(body, indent=4)
r = s.post(url, data=data, headers=headers, cookies=auth.cookies)
alarms = json.loads(r.text)

# Iterates through list of appliances and interfaces, searches through all alarms to match
# if there is an alarm that matches the appliance ID, interface, and alert type of Warning 
for network_id, interface in zip(network_ids,interfaces):
	for alert in alarms:
		if alarm_id in alert.values() and interface in str(alert['source']) and network_id == alert['applianceId']:
			print(alert['hostName'])
			print(alert['source'])
			# Prints the date in UTC
			print('Date:', datetime.datetime.fromtimestamp(alert['timeOccurredInMills'] / 1000.0, tz=datetime.timezone.utc))


# # Logout of Orchestrator and invalidate cookie
r = s.get(logout_url, headers={'Content-Type': 'application/json'}, verify=False)
print('')
print(r.text)