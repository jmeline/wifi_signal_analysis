#!/bin/bash

if [ ! -d ~/miniconda3/wifi ] then
    conda create -n wifi python=3 pandas;
fi

source wifi activate

