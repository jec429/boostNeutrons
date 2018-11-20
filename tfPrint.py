import ROOT,sys,math

c_data = ROOT.TChain("NukeCCQETwoTrack");
c_data.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00022000-00022010.root");

ls = c_data.GetListOfLeaves()



leaves = [str(l).split('"')[1] for l in ls if 'truth' not in str(l) and 'Interpretation' not in str(l)]
#print leaves


c_mc = ROOT.TChain("NukeCCQETwoTrack");
c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00122000-00122005.root");

nhists = [[x,[],'',None] for x in leaves[:-2]]
#nhists = [[x,[],'',None] for x in leaves[:10]]
nhistsv = []
#f = open('neutronDump'+mode+'.csv','w')
f = open('testDump.csv','w')




iev = 0
strings = []
for e in c_mc:
    string = ''
    iev += 1
    nl = 0
    if iev%100 == 0: print (str(iev)+'/'+str(c_mc.GetEntries()))
    #if iev == 201: break
    if e.mc_nFSPart == 2 and (e.mc_FSPartPDG[0] == 2112 or e.mc_FSPartPDG[1] == 2112):
        sig = '0'
    else:
        neutron = False
        for p in e.mc_FSPartPDG:
            if p == 2112: neutron = True
        if neutron:
            sig = '1'
        else:
            sig = '2'

    for i,ls in enumerate(nhists):
        l = ls[0]
        x = eval('e.'+l)
        if not isinstance(x, float) and not isinstance(x, int):
            nhists[i][-1] = 10 #len(x)
            y = [z for z in x]
            if len(x) < 10:
                y += [0] * (10 - len(x))
            for z in y[:10]:
                string += str(z) + ','                
                nl += 1
        else:
            string += str(x) + ','
            nhists[i][-1] = 1
            nl += 1
                
    string += sig
    string += '\n'
    strings.append(string)
    #print nl

title = ''
for s in nhists:
    #if 'skip' in s[-1]: continue
    for i in range(s[-1]):
        title += s[0]+'_'+str(i)+','
title += 'class\n'
f.write(title)


for s in strings:
    f.write(s)
f.close()
