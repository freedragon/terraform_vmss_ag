#!/usr/bin/python3
from logconfig import logger
from configuration import config
from InstanceMetadata import InstanceMetadata
import requests, json, os, time, sys, socket

from bearer_token import BearerAuth

# Initializing InstanceMetadata
metadata = InstanceMetadata().populate()
isPendingDelete = metadata.isPendingDelete()


# Initializing InstanceMetadata
metadata = InstanceMetadata().populate()
isPendingDelete = metadata.isPendingDelete()

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
timeSleep = 10

# Check the value of Platform.PendingDeletionTime tag of IMDS
if (isPendingDelete == False):
    logger.info('exit : ' + str(isPendingDelete))
    sys.exit(1)

# Get App GW Backend status check URL and App GW name
appGatewayUrl = config.get('appgw', 'appgw_behealth_url')
appGateway = config.get('appgw', 'appgw_name')

formatted_url = appGatewayUrl.format(subscriptionId = metadata.subscriptionId, \
                resourceGroupName = metadata.resourceGroupName,\
                appGatewayName = appGateway)

# Getting App GW backend health URI
try:
    r = requests.post(formatted_url, headers = {}, auth=BearerAuth(metadata.access_token))
except requests.exceptions.RequestException as e:
    logger.info("error : " + str(e))
    sys.exit(1)

# Waiting for another api to check the result.
time.sleep(timeSleep)
try:
    resp = requests.get(r.headers["Location"], auth=BearerAuth(metadata.access_token))
except requests.exceptions.RequestException as e:
    logger.info("error : " + str(e))
    sys.exit(1)

# Delete VMSS instance
if (resp.status_code == 200):
    pools = resp.json()["backendAddressPools"]
    for pool in pools:
        settings = pool["backendHttpSettingsCollection"]
        for setting in settings:
            servers = setting["servers"]
            for server in servers:
                if (host_ip == server["address"]):
                    health = server["health"]
                    logger.info(host_name + " is " + health)
                    if (health == "Unhealty"):
                        logger.info("Delete " + host_name)
                        #check copying log and stopping custom metric
                        #delete vmss instance

