#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:25:17 2018
@author: krishna
"""
import json
import os
import networkx as nx
from matplotlib import pyplot as pt
# import urllib.request
import requests
import time
import re


def splitingFunction(splitList):
    """
    Split and take dependencies excluding its version
    """
    newlist = []
    for item in splitList:
        split = item.split(':')[0]
        newlist.append(split)
    return newlist


def computeDevDependencies(devList, name):
    """
    Compute development dependencies
    :param devList:
    :return:
    """
    devList = list(devList)
    # if name=='4':
    #     neList=[]
    #     neList=devList[100:250]
    #     devList=[]
    #     devList=neList
    packageNewList = []
    for item in devList:

        if item.startswith("@babel") or item.startswith('babel'):
            item = 'babel'

        elif item.startswith("@types") or item.startswith('types'):

            item = 'types'
        elif item.startswith("@commit"):
            item = "commitlint"

        elif item.startswith("@sinonjs"):
            split = item.split('/')[1]
            strAdd = "sinonjs-"
            split = strAdd + split
            item = split
        elif item.startswith("@std"):
            split = item.split('/')[1]
            strAdd = "std-"
            split = strAdd + split
            item = split
        elif item.startswith("@studio"):
            split = item.split('/')[1]
            strAdd = "studio-"
            split = strAdd + split
            item = split
        elif item.startswith("@octokit"):
            split = item.split('/')[1]
            strAdd = "octokit-"
            split = strAdd + split
            item = split
        elif item.startswith("@shinnn"):
            split = item.split('/')[1]
            strAdd = "shinnn-"
            split = strAdd + split
            item = split
        elif item.startswith("@lerna-test"):
            split = item.split('/')[1]
            strAdd = "lerna-test-"
            split = strAdd + split
            item = split
        elif item.startswith("@mocha"):
            item = "mocha"
        else:
            item = item

        if item.startswith("acorn"):
            item = 'acorn'

        elif item.startswith("ansi"):
            item = 'ansi'

        elif item.startswith("conventional"):
            item = 'conventional'

        elif item.startswith("eslint"):
            item = 'eslint'

        elif item.startswith("grunt"):
            item = 'grunt'

        elif item.startswith("gulp"):
            item = 'gulp'

        elif item.startswith("istanbul"):
            item = 'istanbul'


        elif item.startswith("jest"):
            item = 'jest'

        elif item.startswith("karma"):
            item = 'karma'

        elif item.startswith("unicode"):
            item = 'unicode'

        elif item.startswith("rollup"):
            item = 'rollup'


        elif item.startswith("lerna"):
            item = 'lerna'
        elif item.startswith("webpack"):
            item = 'webpack'

        elif item.startswith("bundle"):
            item = 'bundle-loader'

        elif item.startswith("merge"):
            item = 'merge2'
        elif item.startswith("vinyl"):
            item = 'vinyl'
        elif item.startswith("chai"):
            item = 'chai'
        elif item.startswith("shelljs"):
            item = 'shelljs'
        elif item.startswith("tslint"):
            item = 'tslint'
        elif item.startswith("lerna"):
            item = 'lerna'
        elif item.startswith("intern"):
            item = 'intern'
        elif item.startswith("standard"):
            item = 'standard'
        elif item.endswith('.io') or item.endswith('.js'):
            splitName = item.split('.')[0]
            item = splitName
        else:
            item = item

        with open("/home/krishna/Desktop/filteredEchart/{}.json"
                          .format(item)) as f:
            packageList = json.load(f)["devDependencies"]

            packageNewList.append(packageList)

    finalPackageList = [item for sublist in packageNewList for item in sublist]
    finalPackageList = set(finalPackageList)

    return finalPackageList


if __name__ == '__main__':

    """
    Main program to compute the list of echart development dependencies
    """
    devDepList = {}
    tier = 1
    depthOfTier = 4
    with open("/home/krishna/Desktop/filteredEchart/package.json"
              ) as f:
        startingList = json.load(f)["devDependencies"]

    newList = splitingFunction(startingList)
    devDepList[tier] = newList
    with open("/home/krishna/Desktop/Tier1.txt", "w") as f:
        for item in newList:
            f.write("%s\n" % item)

    while tier < depthOfTier:
        tier = tier + 1
        name = str(tier)
        packageList = computeDevDependencies(newList, name)
        with open("/home/krishna/Desktop/Tier" + name + ".txt", "w") as f:
            for item in packageList:
                f.write("%s\n" % item)

        devDepList[tier] = packageList
        newList = []
        newList = packageList

