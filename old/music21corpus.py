# coding: utf-8

from music21 import corpus, converter, features
from prettytable import PrettyTable
import time
import gc

# mostra todos os compositores do corpus atual do music21 e quantidade de obras
table = PrettyTable(['Composer Dir.', 'Composer Name', 'Number of Works'])
table.align = 'l'
obras = corpus.getWorkReferences()
for o in obras:
    table.add_row([o['composerDir'], o['composer'], len(o['works'])])
print table

# seleção de compositores... mais próximo ao que já fizemos manualmente
#composerDirs = ['monteverdi', 'bach', 'mozart', 'beethoven', 'schoenberg']
composerDirs = ['beethoven']
sel = [[ob for ob in obras if ob['composerDir'] == composerDirs[i]][0]
       for i in range(len(composerDirs))]

# mostra os compositores usados
#table = PrettyTable(['Composer Dir.', 'Composer Name', '# Works', '# Notes', '# Measures'])
table = PrettyTable(['Composer Dir.', 'Composer Name', '# Works'])

table.align = 'l'
for o in sel:
    # num_notas = 0
    # num_measures = 0
    # for w in o['works']:
    #     score = corpus.parse(w)
    #     num_notas += len(score.flat.notes)
    #     vs = score.parts[0]
    #     ms = vs.getElementsByClass('Measure')
    #     num_measures += len(ms)
    #table.add_row([o['composerDir'], o['composer'], len(o['works']), num_notas, num_measures])
    table.add_row([o['composerDir'], o['composer'], len(o['works'])])
print table

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

# mostra as featureExtractors que usaremos da jSymbolic
i = 0
for f in feats[:jSymbolic]:
    print i, 'jSymbolic:', f.__name__
    i += 1
for f in feats[jSymbolic:]:
    print i, 'native:', f.__name__
    i += 1

# extraímos as features de cada obra, guardamos cada uma em um csv em ./tmp
for c in sel:
    i = 0
    for w in c['works']:
        start_time = time.time()
        ds = features.DataSet(classLabel='Composer')
        ds.addFeatureExtractors(feats)
        ds.addData(w, classValue=c['composerDir'])
        print '%s (%s of %s)' % (w, i+1, len(c['works']))

        # processamos o dataset (extraímos as features)
        ds.process()
        # pegamos todas as features calculadas em uma lista (uma linha por obra)
        #feats_list.append(ds.getFeaturesAsList())
        # salvamos as features em um arquivo CSV
        ds.write('tmp/feats_%s_%s.csv' % (c['composerDir'], i))
        del ds
        gc.collect()
        print 'tempo decorrido:', (time.time() - start_time) / 60.
        i += 1
