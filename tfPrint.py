import ROOT,sys,math
import pandas as pd
import numpy as np
import h5py
import os
import sys
import time
from random import shuffle
from nukePlots import pass_cuts,target1_cut

c_data = ROOT.TChain("NukeCCQETwoTrack");
c_data.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/prunedFiles/pruned_NukeCCQETwoTrack_minerva_run00022000-00022010.root");

ls = c_data.GetListOfLeaves()
leaves = [str(l).split('"')[1] for l in ls if 'truth' not in str(l) and 'Interpretation' not in str(l) and 'genie' not in str(l)]
#print leaves

chains = []
for i in range(100):
    print i
    c_mc = ROOT.TChain("NukeCCQETwoTrack");
    c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/prunedFiles/pruned_minerva_0012"+str(6240+i)+"-0012"+str(6241+i)+".root");
    #c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/prunedFiles/pruned_minerva_0012")
    print(c_mc.GetEntries())
    chains.append(c_mc)
    
nhists = [[x.replace('NukeCCQETwoTrack','NCTT'),[],'',None] for x in leaves[:-2] if 'numi' not in x]
#nhists = nhists[:5]
#nhists = [[x,[],'',None] for x in leaves[:10]]
#nhistsv = []
#f = open('neutronDump'+mode+'.csv','w')
#f = open('testDump.csv','w')

iev = 0
strings = []
for e in c_mc:
    iev += 1
    if iev == 2: break
    for i,ls in enumerate(nhists):
        l = ls[0]
        x = eval('e.'+l.replace('NCTT','NukeCCQETwoTrack'))
        if not isinstance(x, float) and not isinstance(x, int):
            nhists[i][-1] = 4 #len(x)
        else:
            nhists[i][-1] = 1

                
title = []
for s in nhists:
    #if 'skip' in s[-1]: continue
    for i in range(s[-1]):
        title.append(s[0]+'_'+str(i))
title += ['class']
#print title

start_time = time.time()
n_cat0 = 0
n_cat1 = 0
n_cat2 = 0
max_cat = 20000

os.system('rm test_QE_5k.h5')
os.system('rm test_QE.h5')
store_5k = pd.HDFStore('test_QE_5k.h5')
store = pd.HDFStore('test_QE.h5')
bdata5k = []

oneNeutron = 0
moreOneNeutron = 1

for ch in chains:
    if n_cat0+n_cat1+n_cat2 > 2*max_cat: break
    start_time_c = time.time()
    iev = 0
    bdata = []
    for e in ch:
        iev += 1
        #if iev > 20: break    
        if not pass_cuts(e): continue
        if not target1_cut(e.vtx[2]): continue
        
        if iev%1000 == 0:
            print (str(iev)+'/'+str(ch.GetEntries()))
            print 'cats=',n_cat0,n_cat1,n_cat2
        #new categories
        #if e.mc_nFSPart == 2 and (e.mc_FSPartPDG[0] == 2112 or e.mc_FSPartPDG[1] == 2112):
        if e.genie_n_muons == 1 and e.genie_n_pions == 0:
            sig = 0
            if n_cat0 > max_cat: continue
            n_cat0 += 1
        else:
            #neutron = False
            #for p in e.mc_FSPartPDG:
            #    if p == 2112: neutron = True
            #if neutron:
            #    sig = 1
            #    if n_cat1 > max_cat: continue
            #    n_cat1 += 1
            #else:
            #    sig = 2
            #    if n_cat2 > max_cat: continue
            #    n_cat2 += 1
            sig = 1
            if n_cat1 > max_cat: continue
            n_cat1 += 1

        data = []           

        for i,ls in enumerate(nhists):
            l = ls[0]
            x = eval('e.'+l.replace('NCTT','NukeCCQETwoTrack'))
            if not isinstance(x, float) and not isinstance(x, int):
                y = [z for z in x]
                if len(x) < 10:
                    y += [0] * (4 - len(x))
                for z in y[:4]:
                    data.append(float(z))                
            else:
                data.append(float(x))

        data.append(sig)
        bdata.append(data)
        if (sig == 0 and n_cat0 < 1500) or (sig == 1 and n_cat1 < 1500) or (sig == 2 and n_cat2 < 1500):
            bdata5k.append(data)

    shuffle(bdata)
    df = pd.DataFrame(bdata , columns=title)       
    store.append('df', df)
    
    print("--- %s seconds ---" % (time.time() - start_time_c))

shuffle(bdata5k)
df_5k = pd.DataFrame(bdata5k , columns=title)        
store_5k.append('df', df_5k)


print("--- %s seconds total ---" % (time.time() - start_time))
        
store.close()
store_5k.close()
