import ROOT,sys,math
import pandas as pd
import numpy as np
import h5py
import sys
import time

c_data = ROOT.TChain("NukeCCQETwoTrack");
c_data.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00022000-00022010.root");

ls = c_data.GetListOfLeaves()



leaves = [str(l).split('"')[1] for l in ls if 'truth' not in str(l) and 'Interpretation' not in str(l) and 'genie' not in str(l)]
#print leaves

c_mc = ROOT.TChain("NukeCCQETwoTrack");
c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00122000-00122005.root");

nhists = [[x.replace('NukeCCQETwoTrack','NCTT'),[],'',None] for x in leaves[:-2] if 'numi' not in x]
#nhists = [[x,[],'',None] for x in leaves[:10]]
nhistsv = []
#f = open('neutronDump'+mode+'.csv','w')
f = open('testDump.csv','w')



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

store_5k = pd.HDFStore('test_5k.h5')
store = pd.HDFStore('test.h5')
#print title

iev = 0

bdata = []

bev = 0
start_time = time.time()
for e in c_mc:
    iev += 1
    #if iev < 100*bev: continue
    #if iev > 100*(bev+1): break
    if iev > 5000: break
    if iev%100 == 0: print (str(iev)+'/'+str(c_mc.GetEntries()))
    if e.mc_nFSPart == 2 and (e.mc_FSPartPDG[0] == 2112 or e.mc_FSPartPDG[1] == 2112):
        sig = 0
    else:
        neutron = False
        for p in e.mc_FSPartPDG:
            if p == 2112: neutron = True
        if neutron:
            sig = 1
        else:
            sig = 2

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
    #print iev#,data
    bdata.append(data)
    
df = pd.DataFrame(bdata , columns=title)        
df_5k = pd.DataFrame([d[:5000] for d in bdata] , columns=title)        
store.append('df', df)
store_5k.append('df', df_5k)
print("--- %s seconds ---" % (time.time() - start_time))

store.close()
store_5k.close()
