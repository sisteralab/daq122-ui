#! /bin/bash

pyinstaller main.py --clean -n DAQ122 --onedir --icon="./assets/logo.ico" --noconsole -y --add-data="assets:assets" --add-data="daq122.so:." --add-data="libdaq-2.0.0.dll:."