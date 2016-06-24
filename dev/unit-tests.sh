#!/bin/bash

find . -name *.pyc -delete
echo
echo "Running Specs"
echo "----------------------------------------------------------------------"
echo
mamba -f progress `find . -maxdepth 2 -type d -name "specs" | grep -v systems`
MAMBA_RETCODE=$?

exit $(($MAMBA_RETCODE))