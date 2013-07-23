# coding: utf-8

# usando o corpus da pesquisa scarlatti=>beethoven

from music21 import corpus, converter, features
from time import time

compositores = ['beethoven', 'mozart', 'scarlatti']
tss = []

# coloca em feats apenas as featuresExtractors do jSymbolic já implementadas
feats = []
fs = features.jSymbolic.extractorsById
for k in fs:
    for i in range(len(fs[k])):
        if fs[k][i] is not None:
            n = fs[k][i].__name__
            if fs[k][i] in features.jSymbolic.featureExtractors:
                feats.append(fs[k][i])
# coloca em feats as featureExtractors nativas do music21
jSymbolic = len(feats)
feats += features.extractorsById('all', library='native')

for compositor in compositores:
    corpus = open('../scar/corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    comps = {}
    
    # para cada sonata
    for hum in hums:
        start_time = time()
        print 'obra: %s de: %s' % (hum,compositor)
        print '-' * 80
        
        # importamos a sonata
        opus = converter.parse('../scar/corpus_%s/%s' % (compositor,hum))

        ds = features.DataSet(classLabel='Composer')
        ds.addFeatureExtractors(feats)
        ds.addData(opus, classValue=compositor)
        ds.process()
        l = ds.getFeaturesAsList()
        print l
        ds.write('tmp/feats_%s_%s.csv' % (compositor, hum))
        #f = features.allFeaturesAsList(opus)
        #print f
        print 'tempo:', (time() - start_time) / 60.
