# coding: utf-8

# usa os valores de features salvos em arquivos CSV em tmp/ para plotar os
# resultados (projeção LDA)

from music21 import converter, features
import numpy as np
import pylab as py
import matplotlib.pyplot as plt

from sklearn.lda import LDA
#from sklearn.decomposition import PCA

compositores = ['scarlatti', 'haydn', 'mozart', 'beethoven']

# abre um arquivo CSV qualquer apenas para ter a lista de ids
f = open('tmp/feats_beethoven_sonata01-1.krn.csv')
ls = f.readlines()
I = ls[0].split(',')
I = ['Composer', 'Work'] + I[1:-1]
f.close()

# T contém a tabela de valores de features, uma linha para cada sonata, uma
# coluna para cada feature
T = []
y = []
c_comp = 0
for compositor in compositores:
    # abrimos a listagem do corpus para podermos consultar cada feature salva
    # no respectivo arquivo CSV
    corpus = open('corpus/corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    comps = {}
    print 'Compositor: %s. Obras: %s' % (compositor.capitalize(), len(hums))
    # para cada sonata...
    for hum in hums:
        # abrimos o CSV...
        f = open('tmp/feats_%s_%s.csv' % (compositor, hum))
        ls = f.readlines()
        lt = ls[1].split(',')
        # primeira coluna: compositor, segunda coluna: obra, resto: valores
        vs = [compositor, hum]
        vs += [float(lt[i]) for i in range(1, len(lt)-1)]
        T.append(vs)
        f.close()
        y.append(c_comp)
    c_comp += 1

Ti = np.array(T)
T = np.array(Ti[:,2:], dtype=float)
# cols = [2,3]
# F__ = T[:,cols]
F__ = T

# normalizamos
M = np.mean(F__, axis=0)
D = np.std(F__, axis=0)
F = np.nan_to_num((F__-M) / D)

### LDA ###

X = F
y = np.array(y) # classes
target_names = np.array(compositores)

# pca = PCA(n_components=2)
# X_r2 = pca.fit(X).transform(X)

for i in xrange(X.shape[1]):
    X[:,i] = (X[:,i] - X[:,i].mean())/X[:,i].std()

X = np.nan_to_num(X)
lda = LDA(n_components=2)
X_r2 = lda.fit(X, y).transform(X)
print 'coeficientes LDA:', lda.coef_
print X_r2

# calculamos os protótipos, um para cada grupo de obras (um por compositor)
# um protótipo é o ponto médio do grupo de sonatas, é o ponto que "representa"
# o compositor
Fs = []
Prots = []
for i in range(len(compositores)):
    Fs.append(X_r2[y == i])
    prot = np.array([np.mean(X_r2[y==i, k]) for k in range(X_r2.shape[1])])
    prot = np.nan_to_num(prot)
    Prots.append(prot)

principais = np.array(Prots)

# plotamos a série temporal
plt.figure(figsize=(12,12))
ax = plt.subplot(111)
for i in range(len(compositores)):
    x = Prots[i][0]
    y = Prots[i][1]
    aaf = np.sum(Prots[:i+1], 0) / (i+1)
    ax.plot(aaf[0], aaf[1], 'o', color="#666666")
    if i != 0:
        ax.plot((aat[0], aaf[0]), (aat[1], aaf[1]), ':', color='#333333')
    aat = np.copy(aaf)
    ax.plot(x, y, 'bo')
    ax.text(x, y, str(i+1) + ' ' + compositores[i], fontsize=11)

    # plotamos também as sonatas todas
    ax.plot(Fs[i][:,0], Fs[i][:,1], 'o',
            label=compositores[i],
            color=py.cm.jet(np.float(i) / (len(Fs)+1)), alpha=.4)
    # plotamos o protótipo (ponto médio)
    ax.plot(Prots[i][0], Prots[i][1], 'k+')

Prots = np.array(Prots)
ax.plot(Prots[:,0], Prots[:,1], c='#000000')
plt.legend()
plt.title('LDA')
plt.savefig('g1.png')

### DIALETICA, OPOSICAO E INOVACAO (MEDIDAS) ###

agents = compositores
dados = np.array(Prots)
ncomp = len(compositores)
ncarac = 2

#
# Oposição e Inovação
#

for i in xrange(dados.shape[1]):
    dados[:,i] = (dados[:,i] - dados[:,i].mean())/dados[:,i].std()

princ_orig = dados
# para todos
oposicao=[]
inovacao=[]
for i in xrange(1, ncomp):
    a=princ_orig[i-1]    # conforme no artigo... a eh vi
    b=np.sum(princ_orig[:i+1],0)/(i+1) # meio   ... b eh a (average state)
    c=princ_orig[i] # ... c eh um vj

    Di=2*(b-a) # ... Di = 2 * a - vi
    Mij=c-a # ... Mij = vj - vi

    opos=np.sum(Di*Mij)/np.sum(Di**2)  # ... Wij = < Mij , Di > / || Di || ^ 2
    oposicao.append(opos)

    ########## Cálculo de inovação ##################
    # http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    inov = np.sqrt((np.sum((a-c)**2)*np.sum((b-a)**2) -
                    np.sum( (a-c)*(b-a) )**2 ) / np.sum((b-a)**2))

    inovacao.append(inov)

#
# Dialética
#

dialeticas=[]

for i in xrange(2, ncomp):
    a=princ_orig[i-2] # thesis
    b=princ_orig[i-1] # antithesis
    c=princ_orig[i]   # synthesis

    # cálculo da dialética
    t1 = np.sum((b-a)*c)
    t2 = np.sum(-((b**2 - a**2)/2))
    t3 = np.sum((b-a)**2)
    dist = np.abs(t1 + t2) / np.sqrt(t3)

    dialeticas.append(dist)

print '\n###TABLE VII. TABLE VIII###.\n'
print '\n*** Oposição:\n', oposicao
print '\n*** Inovação:\n', inovacao
print '\n*** Dialética:\n', dialeticas

oposicao = np.nan_to_num(oposicao)
inovacao = np.nan_to_num(inovacao)
dialeticas = np.nan_to_num(dialeticas)

# plotando opos, inov e dial
fig = plt.figure(figsize=(13,12))
ax = fig.add_subplot(111)
ax.plot(range(len(oposicao)), oposicao, label="Oposicao")
for i in range(len(oposicao)):
    ax.text(i, oposicao[i], '%.2f' % oposicao[i], fontsize=11)
ax.plot(range(len(inovacao)), inovacao, label="Inovacao")
for i in range(len(inovacao)):
    ax.text(i, inovacao[i], '%.2f' % inovacao[i], fontsize=11)
plt.xticks(range(len(inovacao)), [r'Scarlatti $\rightarrow$ Haydn',
                                  r'Haydn $\rightarrow$ Mozart',
                                  r'Mozart $\rightarrow$ Beethoven'])
fig.autofmt_xdate()
#ax.set_yticklabels([])
plt.legend()
plt.savefig("oposEinov.png")

plt.clf()
ax = fig.add_subplot(111)
ax.plot(range(len(dialeticas)), dialeticas, label="Dialetica")
for i in range(len(dialeticas)):
    ax.text(i, dialeticas[i], '%.2f' % dialeticas[i], fontsize=11)

dialabels = [r'Scarlatti $\rightarrow$ Haydn $\rightarrow$ Mozart',
             r'Haydn $\rightarrow$ Mozart $\rightarrow$ Beethoven']

plt.xticks(range(len(dialeticas)), dialabels)
fig.autofmt_xdate()
plt.legend()
plt.savefig("dialetica.png")

