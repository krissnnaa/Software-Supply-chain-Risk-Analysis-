#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 17:21:09 2018

@author: krishna
"""
import glob2
#Creating a list of path for each python file
pyFilesPath = glob2.glob('/home/krishna/Desktop/fall 2018-19/Research/ipythonProject/**/*.py')

# Reading the libraries from each of the python files
firstTierList=[]
pyFilesPath.remove("/home/krishna/Desktop/fall 2018-19/Research/ipythonProject/ipython/IPython/core/tests/nonascii.py")
for file in pyFilesPath:
    with open(file) as fs:
                for line in fs:
                    if len(line)>=2:                      
                        match = line.split(' ')[0]                       
                        if match=="import" or match=="from": 
                           libMatch = line.split(' ')[1]
                           cnt=0
                           for item in firstTierList:
                               if item ==libMatch:
                                   cnt=1
                           if cnt==0:
                               firstTierList.append(libMatch)
                               
#Extract only pakages from the list and exclude classes
checkChar='.'
finalList=[]
for item in firstTierList:
    flag=0
    for charecter in item:
        if charecter==checkChar:
            flag=1
            break
    if flag==0:
        finalList.append(item)
    else:
        wordSplit=item.split('.')[0]
        finalList.append(wordSplit)
finalList=list(set(finalList))
        
    
