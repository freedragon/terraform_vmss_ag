##!/bin/bash

# create a folder for custom script and checkout code
cd ~
mkdir scripts
cd scripts

#install python  Dependencies
apt update
apt -y dist-upgrade
apt update
apt -y install python3-pip
pip3 install psutil bottle configparser Flask msrestazure azure-mgmt-resource azure-mgmt-compute

#checkout code
git clone https://github.com/bedro96/terraform_vmss_ag.git

#Start health probe job
cd terraform_vmss_ag
chmod +x *.py
nohup ./health_probe_handler.py & echo $! > health-probe-pid.file &

# Schedule cron jobs
crontab crons.sh