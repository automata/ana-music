# coding: utf-8

from music21 import converter, features

s = converter.parse('corpus/mpb/noel_rosa/com-que-roupa.mid')
#s = converter.parse('corpus/classical/scarlatti/scarlatti-d_esserciso_1_(c)icking-archive.xml')
f = features.allFeaturesAsList(s)
print f, len(f[0]) + len(f[1])
# ds = features.DataSet(classLabel='Musician')
# fes = features.extractorsById(['q11', 'q12', 'q13'])
# ds.addFeatureExtractors(fes)

# ds.addData('corpus/mpb/noel_rosa/com-que-roupa.mid', classValue='Noel Rosa')
# ds.process()

