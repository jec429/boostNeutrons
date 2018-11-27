import matplotlib
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
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

def readClasses(fname):
    feats = []
    i = 0
    f = open(fname)
    c = csv.reader(f)
    row0 = next(c)
    lines = np.array([ [float(x) for x in row] for row in csv.reader(f)])
    for i,r in enumerate(row0):
        categs = []
        print(r)
        #if i > 5: break
        feat = Feature()
        feat.index = i
        feat.name = r
        lfeat = []
        for j,row in enumerate(lines):
            #if j%100 == 0: print('%d/%d' %(j,len(lines)))
            categs.append((row[-1]))
            lfeat.append(float(row[i]))
        #print(lfeat)
        #print(categs)
        #lfeat = normalizeFeature(lfeat)
        feat.mean = np.mean(np.array(lfeat))
        feat.STD = np.std(np.array(lfeat))
        if feat.mean == 0 and feat.STD == 0: continue
        feat.histo = histoFeature(lfeat,categs,feat.name)
        #print("Feature = %d %s %f" %(feat.index,feat.name,feat.mean))
        feats.append(feat)
    return feats
        
def histoFeature(dataF,categ,hname):
    #dataF = readData(fname,hindex)
    #categ = readData(fname,-1)
    #print(dataF)
    #print(categ)
    x = [p for p,c in zip(normalizeFeature(dataF),categ) if c == 0 ]
    y = [p for p,c in zip(normalizeFeature(dataF),categ) if c == 1 ]
    z = [p for p,c in zip(normalizeFeature(dataF),categ) if c == 2 ]
    
    fig, ax = plt.subplots()

    #if 'class' in dataF[0]:
    #    bins = np.linspace(0.0, 2.0, 100)
    #else:
    bins = np.linspace(-1.0, 1.0, 100)

    plt.hist(x, bins, alpha=0.5, label='Cat 0')
    plt.hist(y, bins, alpha=0.5, label='Cat 1')
    plt.hist(z, bins, alpha=0.5, label='Cat 2')
    plt.legend(loc='upper right')
    plt.xlabel(hname)
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
    
#h = histoFeature(data,names[hindex])

class Feature():
    def __init__(self, *args, **kwargs):
        self.index = -1
        self.name = ''
        self.STD = 0.0
        self.mean = 0.0
        self.histo = None
        self.status = 0 
