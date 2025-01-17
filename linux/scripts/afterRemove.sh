#!/bin/bash
#
# A shell option that causes the shell to exit immediately if a command exits with a non-zero status.
set -e
# if directory /opt/bunkerweb/ exists then remove it
if [ -d /opt/bunkerweb/ ]; then
    echo "Removing /opt/bunkerweb/ ..."
    rm -rf /opt/bunkerweb/
    echo "Done !"
fi
# if directory /etc/systemd/system/bunkerweb.service exists then remove it
if [ -f /etc/systemd/system/bunkerweb.service ]; then
    echo "Removing /etc/systemd/system/bunkerweb.service ..."
    rm -f /etc/systemd/system/bunkerweb.service
    echo "Done !"
fi
# if directory /etc/systemd/system/bunkerweb-ui.service exists then remove it
if [ -f /etc/systemd/system/bunkerweb-ui.service ]; then
    echo "Removing /etc/systemd/system/bunkerweb-ui.service ..."
    rm -f /etc/systemd/system/bunkerweb-ui.service
    echo "Done !"
fi

# Detect OS between Debian, Ubuntu, CentOS, Fedora 
if [ -f /etc/debian_version ]; then
    # Loop to erase all the files in /etc/nginx/
    for i in $( ls /etc/nginx/ ); do
        echo "Removing /etc/nginx/$i ..."
        rm -rf /etc/nginx/$i
        echo "Done !"
    done
    echo "If you want to reinstall nginx, please run the following command:"
    echo "sudo apt-get install nginx"
elif [ -f /etc/centos-release ]; then
    # Loop to erase all the files in /etc/nginx/
    for i in $( ls /etc/nginx/ ); do
        echo "Removing /etc/nginx/$i ..."
        rm -rf /etc/nginx/$i
        echo "Done !"
    done
    echo "If you want to reinstall nginx, please run the following command:"
    echo "sudo yum install nginx"
elif [ -f /etc/fedora-release ]; then
    # Loop to erase all the files in /etc/nginx/
    for i in $( ls /etc/nginx/ ); do
        echo "Removing /etc/nginx/$i ..."
        rm -rf /etc/nginx/$i
        echo "Done !"
    done
    echo "If you want to reinstall nginx, please run the following command:"
    echo "sudo dnf install nginx"
elif [ -f /etc/lsb-release ]; then
    # Loop to erase all the files in /etc/nginx/
    for i in $( ls /etc/nginx/ ); do
        echo "Removing /etc/nginx/$i ..."
        rm -rf /etc/nginx/$i
        echo "Done !"
    done
    echo "If you want to reinstall nginx, please run the following command:"
    echo "sudo apt-get install nginx"
else
    echo "Your OS is not supported"
    exit 1
fi

# if previous command was successful then restart systemd unit
if [ $? -eq 0 ]; then
    echo "Restarting systemd ..."
    systemctl daemon-reload
    echo "Done !"
fi