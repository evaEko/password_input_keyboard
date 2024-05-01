#!/bin/bash

#install arduino-cli
mkdir install_tmp
cd install_tmp
wget -qO arduino-cli.tar.gz https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_64bit.tar.gz
tar xf arduino-cli.tar.gz -C /usr/local/bin arduino-cli
arduino-cli version

arduino-cli core update-index
arduino-cli core install arduino:avr

cd ..
rm -rf install_tmp
