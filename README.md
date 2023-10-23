# change_dhcp_helpers.py
This script will delete an old DHCP helper and replace it with a specified new one.

## Usage
You will need to fill in variables at the top of the script and fill out the ids.txt file with 1 appliance ID per line:

- *new_dhcp_server* -> The DHCP server you are replacing the old one with.
- *old_dhcp_server* -> The DHCP server being replaced.
- *orchestrator_fqdn* -> Your orchestrator FQDN.

```python
python3 change_dhcp_helpers.py
```

*python3 change_dhcp_helpers.py*

*Username: me@me.com*

*Password:*

*10.77.52.236 has been found and replaced under this interface: 10.10.10.10*

*Deployment configuration successfully applied*

*logged out successfully*

# get_loopback_ips.py

This script will get loopback interface and output the loopback, hostname, networkid into a csv file.

## Usage
You will need to fill in the fqdn variable at the top of the script:

- *orchestrator_fqdn* -> Your orchestrator FQDN.

# replace_all_dhcp_helpers.py

## Usage
You will need to fill in the fqdn variable at the top of the script, the ids.txt and the DHCP server list:

- *orchestrator_fqdn* -> Your orchestrator FQDN.
- *new_dhcp_servers* -> List of DHCP servers to overwrite all existing servers. This will delete all the current servers and replace them with the ones in this list.

### replace_all_dhcp_helpers_specific_interfaces.py ##
Create a file named **ids.csv** and fill it in with the Silver Peak ID and the subnet of the interface you want to update the helpers.
For example it should look like this:

999.NE,10.202.101.0/24  
123.NE,10.202.103.0/24  
321.NE,10.10.10.0/24  

The first value is the ID of the silver peak, and the second value is the subnet of the interface you want to update the DHCP helpers on. So in this example it will only change the helpers on the interfaces in the subnet 10.202.101.0/24, 10.202.103.0/24, 10.10.10.0/24. It will loop through each interface until there's a match, if there is no match, the config makes no changes.


### dhcp_renew.py ##
Fill out the FQDN of your orchestrator at the top, save it and then run. It will ask for 3 variables your API key that needs to have read/write access, the ID of the Silver Peak device, and the interface that will be bounced.

```python
python3 dhcp_renew.py
API KEY: XXXXXXX
Device ID: XX.YY
Interface: wan1
Shutting down wan1
200
Pausing for 5 seconds to allow Orchestrator to execute change...
Turning up interface wan1
200
```

### deployment.py 
Fill out the deployment_ips.csv and the vrrp.csv files with your information. Ensure you have the necessary modules installed in Python. The format of the deployment_ips.csv is 

| label  | IP | mask  | vlan | relay | dhcp1 | dhcp2 |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 5 | 10.10.10.10 | 24 | 33 | n | |
| 5 | 10.20.30.40 | 24 | 177 | y | 10.9.8.7 | 10.6.5.4 |

The label corresponds to the label of the interface, the IP is the physical IP of the silver peak, mask is in slash notation without the forward slash, vlan is VLAN ID, relay is ‘y’ or ‘n’ and the dhcp1 & dhcp2 are the relay servers if you used ‘y’

The vrrp.csv format is 

| groupID  | vip | interface | 
| ------------- | ------------- | ------------- | 
|1 | 10.10.10.1 | lan0.33 |
| 2 | 10.20.20.1 | lan0.177 |

The valid group IDs are 1 – 255 they should be unique for each subnet, but do not have to correlate with VLAN ID to group ID.