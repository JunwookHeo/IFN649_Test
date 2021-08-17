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
sudo yum -y install mosquitto
if [ $? -eq 0 ]
then
    echo "Installation success"
else
    echo "Installation error"
fi
