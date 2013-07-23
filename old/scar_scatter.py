# encoding: utf-8

import pickle as pk
import numpy as np
#import pca as pc
import pylab as py
#import config as conf
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as image

# matriz de dados (feature matrix)
compositores = ['scarlatti', 'haydn', 'mozart', 'beethoven']

# abre um arquivo CSV qualquer apenas para ter a lista de ids
f = open('tmp/feats_beethoven_sonata01-1.krn.csv')
ls = f.readlines()
I = ls[0].split(',')
I = ['Composer', 'Work'] + I[1:-1]
f.close()

T = []
y = []
c_comp = 0
for compositor in compositores:
    corpus = open('../scar/corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    comps = {}
    print 'Compositor: %s. Obras: %s' % (compositor.capitalize(), len(hums))
    # para cada sonata
    for hum in hums:
        f = open('tmp/feats_%s_%s.csv' % (compositor, hum))
        ls = f.readlines()
        lt = ls[1].split(',')
        # primeira coluna: compositor, segunda coluna: obra
        vs = [compositor, hum]
        vs += [float(lt[i]) for i in range(1, len(lt)-1)]
        T.append(vs)
        f.close()
        y.append(c_comp)
    c_comp += 1

Ti = np.array(T)
T = np.array(Ti[:,2:], dtype=float)
F__ = T

# normalizamos
M = np.mean(F__, axis=0)
D = np.std(F__, axis=0)
F = np.nan_to_num((F__-M) / D)

# número de features
Nf = F.shape[1]
print 'número de features', Nf, Nf

### SCATTER MATRIX PARA PARES POSSIVEIS

# combinações de Nf elementos tomados 2 a 2, sem repetições e iguais
w = []
for x in itertools.product(range(Nf), range(Nf)):
    if (len(x) == len(set(x))) and (tuple(reversed(x)) not in w):
        w.append(x)

print 'num combinacoes:', len(w)

# analisamos alpha para cada combinação de NfxNf
alphas = []
for a,b in w:
    # número de classes diferentes
    Nc = 12
    # número de features (como temos pares a,b de features, é 2)
    Nf = 2
    # par de features a,b que iremos analisar
    F_ = F[:,[a,b]]
    # separamos em 12 classes, 20 pinturas para cada pintor
    Fs = [F_[i:i+20] for i in range(0,240,20)]
    
    # global mean feature vector
    # vetor contendo a média de todos os objetos
    M = np.mean(F_, axis=0).reshape((1,Nf))
    # global std feature vector
    D = np.std(F_, axis=0).reshape((1,Nf))
    
    # mean feature vector para cada classe
    Ms = [np.mean(Fs[i], axis=0).reshape((1,Nf)) for i in range(Nc)]
    # std feature vector para cada classe
    Ds = [np.std(Fs[i], axis=0).reshape((1,Nf)) for i in range(Nc)]
    
    # total scatter matrix
    S = ((F_-M).T).dot(F_-M)
    
    # scatter matrix para cada classe
    Ss = [((Fs[i]-Ms[i]).T).dot(Fs[i]-Ms[i]) for i in range(Nc)]
    
    # intraclass scatter matrix
    Sintra = np.array(sum(Ss))

    # quantidade de objetos (linhas) em cada classe
    Ns = [Fs[i].shape[0] for i in range(Nc)]
    # interclass scatter matrix
    Sinter = sum([Ns[i]*(((Ms[i]-M).T).dot(Ms[i]-M)) for i in range(Nc)])

    # validando... S == S_
    S_ = Sintra + Sinter
    Sintra = np.nan_to_num(Sintra)
    Sinter = np.nan_to_num(Sinter)
    S_ = np.nan_to_num(S_)
    # quantificando através de um funcional (traço) o quanto os grupos de
    # features estão inter e intra relacionados (proporção)
    if np.linalg.det(Sintra) != 0: # evitando matrizes singulares...
        ratio = Sinter.dot(np.linalg.inv(Sintra))
        alpha = ratio.trace()
        
        alphas.append([alpha, a, b, Fs]) 

# ordenamos os dados por alpha (menor é melhor)
alphas_sorted = sorted(alphas, key=lambda x:x[0], reverse=True)

# scatter plot considerando n pares de medidas, classes sobrepostas
n = 16

plt.figure(figsize=(13,12))
for i in xrange(n):
    alpha, a, b, Fs = alphas_sorted[i]
    ax = plt.subplot(np.round(np.sqrt(n)), np.round(np.sqrt(n)),i+1)
    for j in xrange(len(Fs)):
        if j >= 6:
            marker = 's'
        else:
            marker = 'o'
        ax.plot(Fs[j][:,0], Fs[j][:,1], marker, label=compositores[j],
                color=py.cm.jet(np.float(j) / (len(Fs)+1)))
    plt.title('%s/%s %.3f' % (a,b,alpha), fontsize='small')
    ax.set_xlim((-2,6))
    ax.set_ylim((-4,5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    #print '%i. alpha: %s. eixo-1: %s. eixo-2: %s.' % (i, alpha, a, b)

plt.savefig('scar_scattertodos.png')

# mostrando cada scatter plot, com labels, apenas 5 primeiros
n = 5
plt.figure(figsize=(13,12))
for i in xrange(n):
    plt.clf()
    alpha, a, b, Fs = alphas_sorted[i]
    ax = plt.subplot(111)
    for j in xrange(len(Fs)):
        if j >= 6:
            marker = 's'
        else:
            marker = 'o'
        ax.plot(Fs[j][:,0], Fs[j][:,1], marker, label=compositores[j],
                color=py.cm.jet(np.float(j) / (len(Fs)+1)))
    plt.title('%s/%s %.3f' % (a,b,alpha), fontsize='small')
    #ax.set_xlim((-2,6))
    #ax.set_ylim((-4,5))
    #ax.set_xticklabels([])
    #ax.set_yticklabels([])
    #print '%i. alpha: %s. eixo-1: %s. eixo-2: %s.' % (i, alpha, a, b)
    plt.legend()
    plt.savefig('scar_scatter_par%s.png' % i)

