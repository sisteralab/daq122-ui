#! /bin/bash

pyInstaller main.py -n DAQ122 --onedir --icon="./assets/logo2.png" --noconsole -y --add-data="assets:assets"
cp ./daq122.so ./