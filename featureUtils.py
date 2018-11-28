import matplotlib
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv

def readCSV(fname):
    start_time = time.time()
    csv = np.genfromtxt(fname, dtype=float, delimiter=',', names=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    #return csv
    return featureColumns(csv)

def readTXT(fname):
    start_time = time.time()
    with open(fname) as f:
        lines = np.array([l.split(',') for l in f.read().splitlines()[:1000]])

    #f = open(fname)
    #lines = []
    #for line in f:
    #    lines.append(line.split(','))
        
    #linesNP = np.array(lines)
    #print(linesNP)
    #print(linesNP.T)
    data = {}
    print("--- %s seconds ---" % (time.time() - start_time))

    for n in lines.T:
        data[n[0]] = np.array(n[1:], dtype=np.float32)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
    return featureColumns(data)

def readData(fname,dindex):
    lines = []
    f = open(fname)
    for line in f:
        if 'event' in line: 
            lines.append((line.split(',')[dindex]))
        else:
            lines.append(float(line.split(',')[dindex]))
    #print(lines)
    return lines

def readDataHDF(fname,dindex):
    if dindex > 1499:
        fnameHDF = fname+'_1.hdf5'
        ddindex = dindex - 1500
    elif dindex < 0:
        fnameHDF = fname+'_1.hdf5'
        ddindex = dindex
    else:
        fnameHDF = fname+'_0.hdf5'
        ddindex = dindex
        
    hdf = pd.read_hdf(fnameHDF,'table')
    result = [hdf.columns[ddindex]]
    
    if 'class' in hdf.columns[ddindex]:
        pfeat = np.array(((hdf[hdf.columns[ddindex]])))
        where_are_NaNs = np.isnan(pfeat)
        pfeat[where_are_NaNs] = 0
        result += list(pfeat)
    else:
        pfeat = np.array(((hdf[hdf.columns[ddindex]])))
        where_are_NaNs = np.isnan(pfeat)
        pfeat[where_are_NaNs] = 0
        result += list(normalizeFeature(pfeat))

    return result
        
def readDataHDFBlock(fname,tindex):    
    if tindex > 74:
        fnameHDF = fname+'_1.hdf5'
        ttindex = tindex - 75
    elif tindex < 0:
        fnameHDF = fname+'_1.hdf5'
        ttindex = tindex
    else:
        fnameHDF = fname+'_0.hdf5'
        ttindex = tindex
       
    hdf = pd.read_hdf(fnameHDF,'table')

    block = []
    for i in range(ttindex*20,(ttindex+1)*20):
        feat = [hdf.columns[i]]
        pfeat = np.array(((hdf[hdf.columns[i]])))
        where_are_NaNs = np.isnan(pfeat)
        pfeat[where_are_NaNs] = 0
        feat += list(normalizeFeature(pfeat))
        block.append(feat)
    return block
            
def histoFeature(fname,hindex,fstatus):
    dataF = readDataHDF(fname,hindex)
    categ = readDataHDF(fname,-1)
    #fstatus[hindex] = 0 if np.std(dataF[1:]) == 0 else 1
    #print(dataF)
    #print(categ)
    x = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 0 ]
    y = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 1 ]
    z = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 2 ]

    #print('x',x)
    #print('y',y)
    #print('z',z)
    
    fig, ax = plt.subplots()

    if 'class' in dataF[0]:
        bins = np.linspace(0.0, 2.0, 100)
    else:
        bins = np.linspace(-1.0, 1.0, 100)

    plt.hist(x, bins, alpha=0.5, label='Cat 0')
    plt.hist(y, bins, alpha=0.5, label='Cat 1')
    plt.hist(z, bins, alpha=0.5, label='Cat 2')
    plt.legend(loc='upper right')
    plt.xlabel(dataF[0])
    plt.ylabel('Counts')

    return fig


def removeFeature(data,hname):
    index = findFeature([n[0] for n in data ],hname)
    del data[index]
    return data
    
def findFeature(names,hname):
    index = -1
    for i,n in enumerate(names):
        if hname == n:
            index = i
    return index

def featureColumns(data):
    new_data = []
    if isinstance(data,dict):
        for n in data.keys():
            if'class' not in n:
                feature = normalizeFeature(data[n])
            else:
                feature = np.array(data[n])
            new_data.append([n,feature,1])
    else:
        for n in data.dtype.names:
            if'class' not in n:
                feature = normalizeFeature(data[n])
            else:
                feature = np.array(data[n])
            new_data.append([n,feature,1])
    return featureStatus(new_data)

def normalizeFeature(feat):
    feature = np.array(feat)
    #print(np.max(abs(feature)))
    if np.max(abs(feature)) > 0:
        return feature/np.max(abs(feature))
    else:
        return feature

def featureStatus(ldata):
    new_data = []
    for d in ldata:
        status = 0 if np.std(d[1]) == 0 else 1
        new_data.append([d[0],d[1],status])
    return new_data

def arrayRMS(ar):
    return np.sqrt(np.mean(np.square(ar)))
    
def initStatus(fname):
    sz = 0
    fnameHDF = fname + '_0.hdf5'
    hdf = pd.read_hdf(fnameHDF,'table')
    sz += len(hdf.columns)
    fnameHDF = fname + '_1.hdf5'
    hdf = pd.read_hdf(fnameHDF,'table')
    sz += len(hdf.columns)
    
    return sz*[-1]


def csvToHDF(csv_filename):
    hdf_filename_0 = csv_filename.replace('.csv','_0.hdf5')
    hdf_filename_1 = csv_filename.replace('.csv','_1.hdf5')

    df = pd.read_csv(csv_filename, header=0)
    dfs = np.split(df, [1800], axis=1)
    print(dfs[0]['n_hyps_0'])
    
    dfs[0].to_hdf(hdf_filename_0, 'table',append=False)
    dfs[1].to_hdf(hdf_filename_1, 'table',append=False)
    
class Feature():
    def __init__(self, *args, **kwargs):
        self.index = -1
        self.name = ''
        self.STD = 0.0
        self.mean = 0.0
        self.histo = None
        self.status = 0 
