#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:25:17 2018

@author: eliza
"""
import json
import os
import networkx as nx
from matplotlib import pyplot as pt
#import urllib.request
import requests
import time
import re

def calculate(dl,keyCount,dB):
    """
    function to compute dependecy list
    """
    for key,value in dl.items():
        keyCount=keyCount+1
        pyCheck=[x for x in value if x.startswith('python')]
        if len(pyCheck)==0:
            pythCheck="null"
        else:
            pythCheck=pyCheck[0]
        cnt=0
        for v in value:
            if v !=pythCheck and v:
                dep= [x for x in os.listdir('/home/eliza/anaconda3/pkgs') 
                if x.startswith(v[0:2])]    
                depi=[lst for lst in dep if not lst.endswith('bz2')]
                with open ("/home/eliza/anaconda3/pkgs/{}/info/index.json"
                       .format(depi[0])) as f:
                    lis=json.load(f)["depends"]
                 
                k=0
                for key in dB.keys():
                    if key==v:
                      k=1
                if k!=1:
                    dic[v]=lis
                    cnt=cnt+1
    return dic,keyCount,cnt

def plotSupplyChainNetwork(dB):
    """
    This function plots dependency network of ipython
    """
    G= nx.Graph()
    for key,value in dB.items():
        pyCheck=[x for x in value if x.startswith('python')]
        if len(pyCheck)==0:
            pythCheck="null"
        else:
            pythCheck=pyCheck[0]
        for v in value:
            if v !=pythCheck and v:
                G.add_edges_from([(key,v)])
    nx.draw(G,with_labels=True)
    pt.show()
    
def countDependeincies(dB):
    """
    Counts number of dependecies of each package
    """
    count=[]
    numberDep={}
    numDep={}
    for i in range(len(dB)):
        count.append(0)
    i=0
    for key,value in dB.items():
        depList=[]
        for k,val in dB.items():
            if k==key:
                continue
            else:
                for v in val:
                    if v==key:
                        count[i]=count[i]+1
                        depList.append(k)
        numberDep[key]= count[i]
        numDep[key]=depList
        i=i+1
    return numberDep,numDep


def libDependecyCalculation(libDict,dB,libD):
    """
    lib dependency calculation
    """
    tempDict={}
    ls=[]
    
    for value in libDict.values():
        value=[x for x in value if not x.startswith('python')]
        
        for v in value:
            if v:
                 k=0
                 for key in libD.keys():
                     if key==v:
                         k=1
                 if k!=1:
                     if v=='mkl':
                         v='mkl_random'
                     if v =='numpy >=1.11.3,<2.0a0':
                         v='numpy >=1.10'
                     if v=='libgcc-ng 7.2.0.*':
                         v='libgcc-ng >=7.2.0'
                     if v=='libstdcxx-ng 7.2.0.*':
                         v='libstdcxx-ng >=7.2.0'
                     ls=dB[v]
                     ls=[x for x in ls if not x.startswith('python')]
                     tempDict[v]=ls    

    return tempDict
        
         
def supplyChainRiskMatrices(libdi,dB):
    """
    Supply chain matrixes (number of edge and year)
    considering libgcc package
    """
    numberOfEdge={}
    for key in libdi.keys():
        for keys in dB.keys():
            if key==keys:
                numberOfEdge[key]=dB[key]
    
    return numberOfEdge

def releaseSupplyChainMatrix(depenDict):
    """
    Release date of each pakages
    """
    dateDict={}
    versionDic={}
    for key in depenDict.keys():
        dep= [x for x in os.listdir('/home/eliza/anaconda3/pkgs') 
                if x.startswith(key[0:3])] 
        depi=[lst for lst in dep if not lst.endswith('bz2')]
        with open ("/home/eliza/anaconda3/pkgs/{}/info/index.json"
                       .format(depi[0])) as f:
            lis=json.load(f)["version"]
        versionDic[key]=lis
        dep= [x for x in os.listdir('/home/eliza/anaconda3/pkgs/{}/info'
                                    .format(depi[0])) 
                if x.startswith('LICENSE')] 
        
        if len(dep)!=0:
        
            with open("/home/eliza/anaconda3/pkgs/{}/info/LICENSE.txt"
                           .format(depi[0]), encoding="utf-8") as fs:
                for line in fs:
                    match = re.search(r'\d\d\d\d+.?\d*', line)
                    if match:
                        dateDict[key]=match.group()
        
    return versionDic,dateDict
    
            
def readUsingURL():
    #with urllib.request.urlopen("") as url:
                                
    data=requests.get("https://raw.githubusercontent.com/takluyver/backcall/blob/master/LICENSE")
    print (data)


if __name__=='__main__' :
    
    """
    Main program to compute the list of ipython dependencies
    """
    with open ("/home/eliza/anaconda3/pkgs/ipython-6.4.0-py36_0/info/index.json"
           ) as f:
        li=json.load(f)["depends"]
    dl={}
    dBackup={}
    dl['ipython']=li
    dBackup=dl.copy()
    dic={}
    keyCount=0
    listDic={}
    i=1
    tierDic={}
    li=[x for x in li if not x.startswith('python')] 
    tierDic[i]=li
    libTier={}
    libTier[i]=[]
    while True:
        dic,keyCount,cnt=calculate(dl,keyCount,dBackup)   
        if len(dl)==keyCount:
            dBackup.update(dic)
            tierList=[]
            libList=[]
            for key,value in dic.items():
                tierList.extend(value)
                for val in value:
                    if "libgcc-ng >=7.2.0" == val:
                        libList.append(key)
                        
            tierList=list(set(tierList))
            libList=list(set(libList))
            listDic[i]=dic
            i=i+1
            tierList=[x for x in tierList if not x.startswith('python')]
            libList=[x for x in libList if not x.startswith('python')] 
            tierDic[i]=tierList
            libTier[i]=libList
            
            dl=dic
            dic={}
        keyCount=0
        if cnt ==0:
            break
        
    #Call function to plot supply chain network 
    plotSupplyChainNetwork(dBackup)
    
    #Call function to count number of dependencies
    numberDep, numDep=countDependeincies(dBackup)
        
    #find risk in supplier tier when libgcc package get updated or corrupted
    libList=[]
    for key,value in libTier.items():
        for val in value:
            libList.append(val)
            
    libList=list(set(libList))
    depenDict={}
    tempDic={}
    depenDict['libgcc-ng >=7.2.0']=libList
    tempDic=depenDict.copy()
    while True:
        tempDic=libDependecyCalculation(tempDic,numDep,depenDict)
        depenDict.update(tempDic)
        if len (tempDic)==0:
            break        
    plotSupplyChainNetwork(depenDict)
    
    #suppy chain matrix
    numberofEdge=supplyChainRiskMatrices(depenDict,numberDep)
    print("Number of dependencies on each package:\n")
    print(numberofEdge)
    print("\n\n Version of each package:\n")
    #release version
    versionDic={}
    dateDic={}
    versionDic,dateDic=releaseSupplyChainMatrix(depenDict)
    print(versionDic)
    print("\n\n Date of Release of each package:\n")
    print(dateDic)
    # To compute date from online link
    #readUsingURL()
   
    
                             
                                  
   