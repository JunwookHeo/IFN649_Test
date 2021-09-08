#!/bin/bash

echo "Start Initialization"

echo "Installing epel"
sudo amazon-linux-extras install -y epel
if [ $? -eq 0 ]
then
    echo "Installation success"
else
    echo "Installation error"
fi

echo "Update yum packages"
sudo yum update -y
if [ $? -eq 0 ]
then
    echo "Update success"
else
    echo "Update error"
fi

echo "Installing mosquitto"
sudo yum install -y mosquitto
if [ $? -eq 0 ]
then
    echo "Installation success"
else
    echo "Installation error"
fi

# Check installation
mos=$(mosquitto -h)
echo "Checking mosquitto installation"
if [[ $mos == *"mosquitto version"* ]]
then
    echo "mosquitto installed"
else
    echo "mosquitto not installed"
fi

# Start mosquitto service
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
if [ $? -eq 0 ]
then
    echo "Starting mosquitto service success"
else
    echo "Starting mosquitto service error"
fi
