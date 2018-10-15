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
for files in pyFilesPath:
    with open(files) as fs:
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

# Remove itself packages
temp = []
itselfList = []
start = ('.','%','IPython', 'ipython')
for item in finalList:
    if item.startswith(start):
        itselfList.append(item)
    else:
        temp.append(item)
finalList=temp.copy()

temp1=[]
for item in finalList:
    if item.endswith('\n') or item.endswith(','):
        item = item[:-1]
        temp1.append(item)
    else:
        temp1.append(item)

newfinalList = temp1.copy()
newfinalList = list(set(newfinalList))

# Remove standard libraires to get external libraries
standardList = []
externalList = []
externalList = newfinalList.copy()
externalList.pop(0)
with open('standardLibraries.txt') as fs:
    standardList = fs.read().splitlines()

checkChar = '.'
finalStandardList = []
for item in standardList:
    flag = 0
    for charecter in item:
        if charecter == checkChar:
            flag = 1
            break
    if flag == 0:
        finalStandardList.append(item)
    else:
        wordSplit = item.split('.')[0]
        finalStandardList.append(wordSplit)
finalStandardList = list(set(finalStandardList))
finalExternalList=[item for item in externalList if item not in finalStandardList]

# Writing final list of first-tier into file
with open("firstExternalLibraries.txt", "w") as f:
    for item in finalExternalList:
f.write("%s\n" % item)

# Creating a list of path for each python file
pyFilesPathSec = glob2.glob('/home/krishna/Desktop/fall 2018-19/Research/ipython-secondTier/**/*.py')
pyFilesPathSec.remove("/home/krishna/Desktop/fall 2018-19/Research/ipython-secondTier/wxPython-master/demo/OGL.py")
# Reading the libraries from each of the python : excluding WXPYTHON-MASTER ogl.py
secondTierList = []
for file in pyFilesPathSec:
    with open(file) as fs:
        for line in fs:
            if len(line) >= 2:
                match = line.split(' ')[0]
                if match == "import" or match == "from":
                    libMatch = line.split(' ')[1]
                    cnt = 0
                    for item in secondTierList:
                        if item == libMatch:
                            cnt = 1
                    if cnt == 0:
                        secondTierList.append(libMatch)

# Extract only pakages from the list and exclude classes
checkChar = '.'
finalList = []
for item in secondTierList:
    flag = 0
    for charecter in item:
        if charecter == checkChar:
            flag = 1
            break
    if flag == 0:
        finalList.append(item)
    else:
        wordSplit = item.split('.')[0]
        finalList.append(wordSplit)
finalList = list(set(finalList))

# Remove itself packages
temp = []
itselfList = []
start = ('.', '%', 'IPython', 'ipython', 'matplotlib', 'pygtk', 'backcall', 'pygments',
         'nose',
         'cython',
         'GliPy',
         'pickleshare',
         'requests',
         'prompt_toolkit',
         'pexpect',
         'simplegeneric',
         'sphinx',
         'wx',
         'clr',
         'pyglet',
         'traitlets',
         'apigen',
         'glob2',
         'docutils',
         'decorator',
         'PyQt4',
         'setuptools',
         'numpy',
         'gtk',
         'wcwidth')
for item in finalList:
    if item.startswith(start):
        itselfList.append(item)
    else:
        temp.append(item)
finalList = temp.copy()

temp1 = []
for item in finalList:
    if item.endswith('\n') or item.endswith(','):
        item = item[:-1]
        temp1.append(item)
    else:
        temp1.append(item)

newfinalList = temp1.copy()
newfinalList = list(set(newfinalList))

# Remove standard libraires to get external libraries
standardList = []
externalList = []
externalList = newfinalList.copy()
externalList.pop(0)

finalExternalList = [item for item in externalList if item not in finalStandardList]

# Writing final list of second-tier into file
with open("secondExternalLibraries.txt", "w") as f:
    for item in finalExternalList:
        f.write("%s\n" % item)
        
