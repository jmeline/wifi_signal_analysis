#!/bin/bash

if [ ! -d ~/miniconda3/wifi ]; then
    conda create -n wifi python=3 pandas pytest;
fi

source /home/jmeline/miniconda3/bin/activate wifi

