#!/bin/bash

for package in $(ls -d */); do pushd $package; if [ -e setup.py ]; then python setup.py develop; fi; popd; done
pip install pip --upgrade
pip install -r requirements.txt --upgrade
pip install -r requirements-dev.txt --upgrade