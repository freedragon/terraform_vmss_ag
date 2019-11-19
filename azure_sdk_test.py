#from azure.identity import ManagedIdentityCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_active_directory import MSIAuthentication

#credentials = ManagedIdentityCredential()
credentials = MSIAuthentication()
subscription_id='05be085b-86ea-4336-addc-38fd56051a9e'
resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)

for item in resource_client.resource_groups.list():
    print(item.name)
rg = 'kunhovmss-rg'
name = 'kunhovmss'
vmss = compute_client.virtual_machine_scale_set_vms.list(rg,name)
for i in vmss:
    print(i.name)

compute_client.virtual_machine_scale_set_vms.delete(rg,name,1)