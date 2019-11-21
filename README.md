# Azure VMSS Lifecycle Hook
This feature enables users to conduct a graceful shutdown on VMSS instance, when it is targeted for deletion. This provides huge flexibility for exceptional case handling on customer code.

## Overall Architecture
![Architecture Image](https://github.com/bedro96/terraform_vmss_ag/blob/master/vmss_lifecycle_img/overall_architecture.png)
Prerequisite  
- The subscription must opt in for this feature.
- EnablePendingDeletion=true tag configured on the VMSS.

## Overall Procedure
![Architecture Image](https://github.com/bedro96/terraform_vmss_ag/blob/master/vmss_lifecycle_img/procedure.png)

## Core components
**Web Service - health_probe_handler**
![Architecture Image](https://github.com/bedro96/terraform_vmss_ag/blob/master/vmss_lifecycle_img/health_probe_handler.png )

**Delete VMSS Instance - delete_vmss_instance**
![Architecture Image](https://github.com/bedro96/terraform_vmss_ag/blob/master/vmss_lifecycle_img/delete_vmss_instance.png)

# Deployment
## Environment
Overall evnironment will be deployed with terraform with following characteristics.  
 - Availability Zone: not considered
 - PublicLB: deployed with a NAT rule for ssh 
 - MSI: Enabled and configured to have yes, MSI RBAC:yes, Custom Extension:yes, PPG:yes, Application Gateway:yes

## Terraform 
Get vmss_ag.tf and variable.tf. Place these files under identical foler. 

```bash
terraform init
terraform plan -out=vmss_ag.out
terraform apply vmss_ag.out
```

## Location of downloaded extension files 
```bash
/var/lib/waagent/custom-script/download/1
```
The script is executed with root privilege.

