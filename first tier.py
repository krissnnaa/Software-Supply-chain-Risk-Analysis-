#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 17:21:09 2018

@author: krishna
"""
import os
import glob2
from pathlib import Path

#Creating a list of path for each python file
pyFilesPath = glob2.glob('/home/krishna/Desktop/fall 2018-19/Research/ipythonProject/**/*.py')

# Reading the libraries from each of the python files
for file in pyFilesPath:
    openFile=open(file,"r")
    
