import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt


def readCSV(fname):
    csv = np.genfromtxt(fname, dtype=float, delimiter=',', names=True)
    #return csv
    return featureColumns(csv)

def histoFeature(data,hname):
    n_bins = 20
    names = [n[0] for n in data]
    dataF = data[findFeature(names,hname)]
    x = [p for p,c in zip(dataF[1], data[-1][1]) if c == 0 ]
    y = [p for p,c in zip(dataF[1], data[-1][1]) if c == 1 ]
    z = [p for p,c in zip(dataF[1], data[-1][1]) if c == 2 ]

    fig, ax = plt.subplots()

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
