#! /bin/bash

pyinstaller main.py -n DAQ122 --onedir --icon="./assets/logo.ico" --noconsole -y --add-data="assets:assets"
cp ./daq122.so ./dist/DAQ122