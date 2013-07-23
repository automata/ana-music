# coding: utf-8

# usando o corpus da pesquisa scarlatti=>beethoven como teste inicial

# features possui os feature extractors do music21
from music21 import converter, features
from time import time

compositores = ['scarlatti', 'haydn', 'beethoven', 'mozart']

# coloca em feats apenas as featuresExtractors do jSymbolic já implementadas
# todas as features estão listadas em https://gist.github.com/automata/5872349
feats = []
fs = features.jSymbolic.extractorsById
for k in fs:
    for i in range(len(fs[k])):
        if fs[k][i] is not None:
            n = fs[k][i].__name__
            if fs[k][i] in features.jSymbolic.featureExtractors:
                feats.append(fs[k][i])

# também coloca em feats as featureExtractors nativas do music21
jSymbolic = len(feats)
feats += features.extractorsById('all', library='native')

# iteramos em cada compositor, e em cada sonata
for compositor in compositores:
    corpus = open('corpus/corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    comps = {}
    
    # para cada sonata...
    for hum in hums:
        # apenas para saber o tempo gasto para extrair as features
        start_time = time()
        print '%s de %s' % (hum,compositor)
        print '-' * 80
        
        # importamos a sonata do diretório do compositor em corpus
        opus = converter.parse('corpus/corpus_%s/%s' % (compositor,hum))

        # criamos um dataset no music21 que guardará os dados dos features
        # extraídos
        ds = features.DataSet(classLabel='Composer')
        # dizemos para o dataset quais as features que deverá usar
        ds.addFeatureExtractors(feats)
        # dizemos para o dataset em qual score (sonata) ele deverá extrair
        ds.addData(opus, classValue=compositor)
        # processamos (isso irá demorar)
        ds.process()
        # pegamos os valores de cada feature extraído como uma lista
        l = ds.getFeaturesAsList()
        print l
        # gravamos em um arquivo CSV esses valores, temporariamente, apenas
        # para garantir que teremos os dados mesmo se o script quebrar
        # o script primeira_fase_ana.py irá ler esses dados posteriormente!
        ds.write('tmp/feats_%s_%s.csv' % (compositor, hum))
        # mostramos o tempo gasto para processar essa sonata
        print 'tempo:', (time() - start_time) / 60.
