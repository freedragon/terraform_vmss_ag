from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from msrestazure.azure_active_directory import MSIAuthentication

credentials = MSIAuthentication()
subscription_id='05be085b-86ea-4336-addc-38fd56051a9e'
resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)

for item in resource_client.resource_groups.list():
    print(item.name)
rg = 'kunhovmss-rg'
name = 'kunhovmss'
vmss = compute_client.virtual_machine_scale_set_vms.list(rg,name)
for i in vmss:
    print(i.name)

#ag_name = 'vmss-appgateway'
#behealth = network_client.application_gateways.backend_health(rg, application_gateway_name)
#print(behealth)

# This will delete the instance.
# compute_client.virtual_machine_scale_set_vms.delete(rg,name,1)
def hostname_to_vmid(hostname):
    # get last 6 characters and remove leading zeroes
    hexatrig = hostname[-6:].lstrip('0')
    multiplier = 1
    vmid = 0
    # reverse string and process each char
    for x in hexatrig[::-1]:
        if x.isdigit():
            vmid += int(x) * multiplier
        else:
            # convert letter to corresponding integer
            vmid += (ord(x) - 55) * multiplier
        multiplier *= 36
    return hostname_to_vmid

# compute_client.virtual_machine_scale_set_vms.delete(rg,name,1)