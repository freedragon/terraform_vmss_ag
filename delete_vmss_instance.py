#!/usr/bin/python3
from logconfig import logger
from configuration import config
from vminstance import VMInstance
import requests, json, os, time, sys
from bearer_token import BearerAuth

import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
timeSleep = 5

vmInstance = VMInstance().populate()

# Check the value of Platform.PendingDeletionTime tag of IMDS

appGatewayUrl = "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/applicationGateways/{appGatewayName}/backendhealth?api-version=2019-09-01"
appGateway = "vmss-appgateway"

formatted_url = appGatewayUrl.format(subscriptionId = vmInstance.subscriptionId, \
                resourceGroupName = vmInstance.resourceGroupName,\
                appGatewayName = appGateway)

# Getting App GW backend health URI
try:
    r = requests.post(formatted_url, headers = {}, auth=BearerAuth(vmInstance.access_token))
except requests.exceptions.RequestException as e:
    print ("error : {0}".format(e))
    sys.exit(1)

# Waiting for another api to check the result.
time.sleep(timeSleep)
try:
    resp = requests.get(r.headers["Location"], auth=BearerAuth(vmInstance.access_token))
except requests.exceptions.RequestException as e:
    print ("error : {0}".format(e))
    sys.exit(1)
    
if (resp.status_code == 200):
    pools = resp.json()["backendAddressPools"]
    for pool in pools:
        settings = pool["backendHttpSettingsCollection"]
        for setting in settings:
            servers = setting["servers"]
            for server in servers:
                if (host_ip == server["address"]):
                    health = server["health"]
                    print('{0} is {1}'.format(host_name, health))
                    if (health == "Unhealty"):
                        print('Delete myself')
                        #check copying log and stopping custom metric
                        #delete vmss instance

