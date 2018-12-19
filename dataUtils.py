import json
import ROOT
import pandas as pd


def data_status():
    c_data = ROOT.TChain("NukeCCQETwoTrack");
    c_data.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00022000-00022010.root");

    hdf = pd.read_hdf('test_5k.h5')
    
    ls = []
    my_dict = {'class':1}
    for l in list(hdf.keys())[:-1]:
        #print l,l[:-2]+'['+l[-1]+']'
        leave = (l[:-2]+'['+l[-1]+']').replace('NCTT','NukeCCQETwoTrack')
        ls.append(leave)
        print l
        my_dict[l] = 0
    
    for l in ls:
        l_dict = (l[:-3]+'_'+l[-2]).replace('NukeCCQETwoTrack','NCTT')
        print l_dict
        c_data.Draw(l)
        h = ROOT.gPad.GetPrimitive("htemp")
        try:
            my_dict[l_dict] = 0 if h.GetStdDev() == 0 else 1
        except:
            print 'Error=',l
        
    with open('my_dict.json', 'w') as f:
        json.dump(my_dict, f)


def compare_best_features():
    f = open('important_features.txt')
    features = []
    for line in f:
        features.append((line.strip()).replace('NCTT','NukeCCQETwoTrack'))

    c_data = ROOT.TChain("NukeCCQETwoTrack");
    c_data.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00022000-00022010.root");

    c_mc = ROOT.TChain("NukeCCQETwoTrack");
    c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00122000-00122005.root");
    c_mc.Add("/Users/hmrbrtzero/Desktop/work/MINERvA/pruned_NukeCCQETwoTrack_minerva_run00122005-00122010.root");

    for l in features:
        #l = features[0]
        l2 = (l[:-2]+'['+l[-1]+']')
        c_data.Draw(l2)
        h_data = ROOT.gPad.GetPrimitive("htemp")
        binmax = h_data.GetMaximumBin()
        x_max = h_data.GetXaxis().GetBinCenter(binmax)

        binmin = h_data.GetMinimumBin()
        x_min = h_data.GetXaxis().GetBinCenter(binmin)
        if x_min < -1e6: x_min = -1e7
        print l,x_min,x_max
        h_d = ROOT.TH1F('h_d',l,100,x_min,x_max)
        h_mc = ROOT.TH1F('h_mc',l,100,x_min,x_max)
        c_data.Draw(l2+">>h_d")
        c_mc.Draw(l2+">>h_mc")
    
        c3 = ROOT.TCanvas('c3')    
        h_d.DrawNormalized('ep')    
        h_mc.SetLineColor(ROOT.kRed)
        h_mc.DrawNormalized('same')
        c3.Print('plots/'+l+'.pdf')
        c3.SetLogy()
        c3.Print('plots/'+l+'_log.pdf')
        h_d = 0
        h_mc = 0
        c3 = 0
        
def main():
    compare_best_features()

if __name__ == "__main__":
    main()



