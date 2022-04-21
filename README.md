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
