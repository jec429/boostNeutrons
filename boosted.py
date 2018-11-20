#!/usr/bin/python
import numpy as np
import scipy.sparse
import pickle
import xgboost as xgb
import matplotlib.pyplot as plt

def main():

    dtrain = xgb.DMatrix('prunedDump.csv?format=csv&label_column=0')
    dtest = xgb.DMatrix('prunedDump.csv?format=csv&label_column=0')
    
    print("Labels")
    print(dtrain.get_label())
    # specify parameters via map, definition are same as c++ version
    param = {'max_depth':6, 'eta':0.3, 'silent':1, 'objective':'multi:softmax', 'num_class':3, 'eval_metric':['merror','mlogloss']}
    #param = {'max_depth':10, 'eta':0.1, 'silent':1, 'objective':'reg:linear'}
    
    # specify validations set to watch performance
    watchlist = [(dtest, 'eval'), (dtrain, 'train')]
    num_round = 10
    bst = xgb.train(param, dtrain, num_round, watchlist)
    
    # this is prediction
    preds = bst.predict(dtest)
    labels = dtest.get_label()
    
    xgb.plot_importance(bst)
    xgb.plot_tree(bst, num_trees=2)
    xgb.plot_tree(bst, num_trees=0)
    #xgb.to_graphviz(bst, num_trees=2)

    
    print(len(preds))
    print(len(labels))

    print(preds[0],preds[1])
    print(labels[0],labels[1])
    
    print('error=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) != int(labels[i])) / float(len(preds))))
    print('accuracy=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == int(labels[i])) / float(len(preds))))
    #plt.show()

    print('0,0=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 0 and  int(labels[i]) == 0)))
    print('0,1=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 0 and  int(labels[i]) == 1)))
    print('0,2=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 0 and  int(labels[i]) == 2)))
    print('1,0=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 1 and  int(labels[i]) == 0)))
    print('1,1=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 1 and  int(labels[i]) == 1)))
    print('1,2=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 1 and  int(labels[i]) == 2)))
    print('2,0=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 2 and  int(labels[i]) == 0)))
    print('2,1=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 2 and  int(labels[i]) == 1)))
    print('2,2=%f' % (sum(1 for i in range(len(preds)) if int(preds[i]) == 2 and  int(labels[i]) == 2)))

    
if __name__ == "__main__":
    main()

    
#bst.save_model('0001.model')
# dump model
#bst.dump_model('dump.raw.txt')
# dump model with feature map
#bst.dump_model('dump.nice.txt', '../data/featmap.txt')
'''
# save dmatrix into binary buffer
dtest.save_binary('dtest.buffer')
# save model
bst.save_model('xgb.model')
# load model and data in
bst2 = xgb.Booster(model_file='xgb.model')
dtest2 = xgb.DMatrix('dtest.buffer')
preds2 = bst2.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds2 - preds)) == 0

# alternatively, you can pickle the booster
pks = pickle.dumps(bst2)
# load model and data in
bst3 = pickle.loads(pks)
preds3 = bst3.predict(dtest2)
# assert they are the same
assert np.sum(np.abs(preds3 - preds)) == 0


###
# build dmatrix from scipy.sparse
print('start running example of build DMatrix from scipy.sparse CSR Matrix')
labels = []
row = []; col = []; dat = []
i = 0
for l in open('../data/agaricus.txt.train'):
    arr = l.split()
    labels.append(int(arr[0]))
    for it in arr[1:]:
        k,v = it.split(':')
        row.append(i); col.append(int(k)); dat.append(float(v))
    i += 1
csr = scipy.sparse.csr_matrix((dat, (row, col)))
dtrain = xgb.DMatrix(csr, label=labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print('start running example of build DMatrix from scipy.sparse CSC Matrix')
# we can also construct from csc matrix
csc = scipy.sparse.csc_matrix((dat, (row, col)))
dtrain = xgb.DMatrix(csc, label=labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)

print('start running example of build DMatrix from numpy array')
# NOTE: npymat is numpy array, we will convert it into scipy.sparse.csr_matrix in internal implementation
# then convert to DMatrix
npymat = csr.todense()
dtrain = xgb.DMatrix(npymat, label=labels)
watchlist = [(dtest, 'eval'), (dtrain, 'train')]
bst = xgb.train(param, dtrain, num_round, watchlist)
'''
