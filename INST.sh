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
echo $mos
if [[ $mos == *"mosquitto version"* ]]
then
    echo "mosquitto installed"
else
    echo "mosquitto not installed"
fi
