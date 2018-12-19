from __future__ import print_function
import matplotlib
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
import xgboost as xgb
import json
import matplotlib.pyplot as plt
import re
from six.moves import range
from matplotlib import rc
from conf_mat_pl import make_conf_mat_plots_rowcolnormonly
from conf_mat_pl import make_conf_mat_plots_raw
from scipy import stats

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
    hdf = pd.read_hdf(fname+'.h5')
    #print(hdf[0])
    result = [hdf.keys()[dindex]]
    
    if 'class' in hdf.columns[dindex]:
        pfeat = np.array(((hdf[hdf.columns[dindex]])))
        where_are_NaNs = np.isnan(pfeat)
        pfeat[where_are_NaNs] = 0
        result += list(pfeat)
    else:
        pfeat = np.array(((hdf[hdf.columns[dindex]])))
        where_are_NaNs = np.isnan(pfeat)
        pfeat[where_are_NaNs] = 0
        result += list(normalizeFeature(pfeat))

    return result
        
def readDataHDFBlock(fname,tindex):           
    hdf = pd.read_hdf(fname+'.h5')

    block = []
    for i in range(tindex*20,(tindex+1)*20):
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
    x = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 0 ]
    y = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 1 ]
    z = [p for p,c in zip((dataF[1:]),categ[1:]) if c == 2 ]

    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(13, 5))
    
    if 'class' in dataF[0]:
        bins = np.linspace(0.0, 2.0, 100)
    elif np.min(dataF[1:]) > 0.5:
        bins = np.linspace(0.5, 1.0, 100)
    elif np.min(dataF[1:]) > 0:
        bins = np.linspace(0.0, 1.0, 100)
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
    if np.max(abs(feat)) > 0:
        feature = feat/np.max(abs(feat))
    else:
        feature = feat
    
    minf = np.min(feature)
    num = (1.-minf) if (1.-minf) != 0 else 1
    featX = np.array([2./num*x+1.-2./num for x in feature])
    #print(np.max(abs(feature)))
    return featX
    
def featureStatus(ldata):
    new_data = []
    for d in ldata:
        status = 0 if np.std(d[1]) == 0 else 1
        new_data.append([d[0],d[1],status])
    return new_data

def arrayRMS(ar):
    return np.sqrt(np.mean(np.square(ar)))
    
def init_status(fname):
    with open('my_dict.json') as f:
        my_dict = json.load(f)
    status = []
    hdf = pd.read_hdf(fname+'.h5')
    for c in hdf.columns:
        #print(c,my_dict[c])
        status.append(my_dict[c])

    #print('status=',len(my_dict),sz)
        
    return status

def update_status(fname,status):
    hdf = pd.read_hdf(fname+'.h5')
    with open('my_dict.json') as f:
        my_dict = json.load(f)

    for i,c in enumerate(hdf.columns):
        #print(c,status[i])
        my_dict[c] = status[i]

    with open('my_dict.json', 'w') as f:
        json.dump(my_dict, f)
    
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

def boosted(num_round):
    ## TRAINING DATASET
    hdf = pd.read_hdf('tmp.h5','train')
    cat = pd.DataFrame(hdf['class'])
    del hdf['class']

    hdf['weight'] = 0
    for c in hdf.columns:
        hdf['weight'] = hdf['weight'] + ((hdf[c] - hdf[c].mean())/hdf[c].std(ddof=0) < 3)
    wei = pd.DataFrame(hdf['weight'])
    weig = [x[0] for x in wei.values]
    #print((weig))
    del hdf['weight']
    dtrain = xgb.DMatrix(hdf,cat)#, weight=weig)

    ## TESTING DATASET
    hdf = pd.read_hdf('tmp.h5','test')
    cat = pd.DataFrame(hdf['class'])
    del hdf['class']
    
    hdf['weight'] = 0
    for c in hdf.columns:
        hdf['weight'] = hdf['weight'] + ((hdf[c] - hdf[c].mean())/hdf[c].std(ddof=0) < 3)
    wei = pd.DataFrame(hdf['weight'])
    weig = [x[0] for x in wei.values]
    #print((weig))
    del hdf['weight']

    dtest = xgb.DMatrix(hdf,cat)#, weight=weig)
    
    print("Labels")
    print(len(dtrain.get_label()))
    print(len(dtest.get_label()))
    # specify parameters via map, definition are same as c++ version
    param = {'max_depth':6, 'eta':0.3, 'silent':1, 'objective':'multi:softmax', 'num_class':3, 'eval_metric':['merror','mlogloss']}
    #param = {'max_depth':10, 'eta':0.1, 'silent':1, 'objective':'reg:linear'}
    
    # specify validations set to watch performance
    watchlist = [(dtest, 'eval'), (dtrain, 'train')]
    #num_round = 5
    bst = xgb.train(param, dtrain, num_round, watchlist)
    preds = bst.predict(dtest)
    labels = dtest.get_label()
        
    #xgb.plot_tree(bst, num_trees=2)
    #xgb.plot_tree(bst, num_trees=0)
    #xgb.to_graphviz(bst, num_trees=2)
    
    print('error=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) != int(labels[i])) / float(len(preds))))
    print('accuracy=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == int(labels[i])) / float(len(preds))))

    return bst

def plot_importance(bst):
    if bst == None:
        print('Boost first!')
        return 0
    ax = xgb.plot_importance(bst, max_num_features=10)
    fig = ax.figure

    f_imp = open('important_features.txt','w')
    labels = list(ax.get_yticklabels())
    labels.reverse()
    for l in labels:
        f_imp.write(l.get_text()+'\n')

    f_imp.close()
    return fig

def get_confusion_matrix(bst):
    if bst == None:
        print('Boost first!')
        return 0
    hdf = pd.read_hdf('tmp.h5','test')
    cat = pd.DataFrame(hdf['class'])
    del hdf['class']
    dtest = xgb.DMatrix(hdf,cat)
    # this is prediction
    preds = bst.predict(dtest)
    labels = dtest.get_label()
    
    l = []
    for i in range(3):
        lj = []
        for j in range(3):
            print(i,j,sum(1 for k in range(len(preds)) if int(preds[k]) == i and  int(labels[k]) == j))
            lj.append(sum(1 for k in range(len(preds)) if int(preds[k]) == i and  int(labels[k]) == j))
        l.append(lj)
    print(l)
    return np.array(l)

def plot_confusion_matrix(matrix):
    #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    #rc('text', usetex=True)
    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif')
    #arr2 = np.array([[914,220,51],[65,390,199],[21,390,750]])
    plot_type_base = 'confusion_matrix_vtxfndr_trainE_testE_'
    plot_type = plot_type_base + str(matrix.shape[0])
    fig = make_conf_mat_plots_raw(matrix, plot_type)
    return fig
    
