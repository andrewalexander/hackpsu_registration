#!/bin/bash

# this is used for the EC2/AutoScaling launch configuration UserData
yum -y install git npm node virtualenv pip --enablerepo epel
git clone https://github.com/andrewalexander/hackpsu_registration
cd hackpsu_registration/
./install.sh 
