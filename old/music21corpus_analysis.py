# coding: utf-8

from music21 import corpus, converter, features
import numpy as np
import pylab as py
import matplotlib.pyplot as plt
import matplotlib.image as image

from sklearn.lda import LDA

composerDirs = ['monteverdi', 'bach', 'mozart', 'beethoven', 'schoenberg']

obras = corpus.getWorkReferences()
sel = [[ob for ob in obras if ob['composerDir'] == composerDirs[i]][0]
       for i in range(len(composerDirs))]

# abre um arquivo CSV qualquer apenas para ter a lista de ids
f = open('tmp/feats_beethoven_0.csv')
ls = f.readlines()
I = ls[0].split(',')
f.close()

T = []
for o in sel:
    i = 0
    for w in o['works']:
        f = open('tmp/feats_%s_%s.csv' % (o['composerDir', i]))
        ls = f.readlines()
        lt = ls[1].split(',')
        # primeira coluna: compositor, segunda coluna: obra
        vs = [o['composerDir'], lt[0]]
        vs += [float(lt[i]) for i in range(1, len(lt)-1)]
        T.append(vs)
        f.close()

T = np.array(T)
cols = [2,3]
F__ = T[:,cols]

# normalizamos
M = np.mean(F__, axis=0)
D = np.std(F__, axis=0)
F = np.nan_to_num((F__-M) / D)

# LDA

X = F
y = np.array([i for i in py.flatten([[i]*20 for i in range(12)])])
target_names = np.array(conf.artistas)

#pca = PCA(n_components=2)
#X_r2 = pca.fit(X).transform(X)

lda = LDA(n_components=2)
X_r2 = lda.fit(X, y).transform(X)

print lda.coef_
print X_r2
# separamos as pinturas em classes de 20 pinturas, uma para cada pintor
# e calculamos os protótipos (pontos médios)
Fs = []
Prots = []
for i in range(12):
    Fs.append(X_r2[y == i])
    prot = np.array([np.mean(X_r2[y==i, k]) for k in range(X_r2.shape[1])])
    prot = np.nan_to_num(prot)
    Prots.append(prot)

# ordenamos a tabela pela ordem correta cronológica dos pintores
Ford = [Fs[conf.ordem[i]] for i in range(12)]
Prots = [Prots[conf.ordem[i]] for i in range(12)]
principais = np.array(Ford)

plt.figure(figsize=(12,12))
ax = plt.subplot(111)
for i in range(12):
    x = Prots[i][0]
    y = Prots[i][1]
    aaf = np.sum(Prots[:i+1], 0) / (i+1)
    ax.plot(aaf[0], aaf[1], 'o', color="#666666")
    if i != 0:
        ax.plot((aat[0], aaf[0]), (aat[1], aaf[1]), ':', color='#333333')
    aat = np.copy(aaf)
    ax.plot(x, y, 'bo')
    ax.text(x, y, str(i+1) + ' ' + conf.artistas[conf.ordem[i]], fontsize=11)

    # plotamos também as pinturas todas
    ax.plot(Ford[i][:,0], Ford[i][:,1], 'o', label=conf.artistas[conf.ordem[i]],
            color=py.cm.jet(np.float(i) / (len(Ford)+1)), alpha=.4)
    # plotamos o protótipo (ponto médio)
    ax.plot(Prots[i][0], Prots[i][1], 'k+')
Prots = np.array(Prots)
ax.plot(Prots[:,0], Prots[:,1], c='#000000')
plt.legend()
plt.title('LDA')
plt.savefig('caso3_g1.png')

# dados usados para cálculo dos 'metrics'
agents = [conf.artistas[conf.ordem[i]] for i in range(12)]
dados = np.array(Prots)
ncomp = 12
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
    inov=np.sqrt(  ( np.sum((a-c)**2)*np.sum((b-a)**2) - np.sum( (a-c)*(b-a) )**2 )/np.sum((b-a)**2)  )

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
dialeticasa = np.nan_to_num(dialeticas)

# plotando opos, inov e dial
fig = plt.figure(figsize=(13,12))
ax = fig.add_subplot(111)
ax.plot(range(len(oposicao)), oposicao, label="Oposicao")
for i in range(len(oposicao)):
    ax.text(i, oposicao[i], '%.2f' % oposicao[i], fontsize=11)
ax.plot(range(len(inovacao)), inovacao, label="Inovacao")
for i in range(len(inovacao)):
    ax.text(i, inovacao[i], '%.2f' % inovacao[i], fontsize=11)
plt.xticks(range(len(inovacao)), [r'Caravaggio $\rightarrow$ Frans Hals',
                                  r'Frans Hals $\rightarrow$ Poussin',
                                  r'Poussin $\rightarrow$ Velazquez',
                                  r'Velazquez $\rightarrow$ Rembrandt',
                                  r'Rembrandt $\rightarrow$ Vermeer',
                                  r'Vermeer $\rightarrow$ Van Gogh',
                                  r'Van Gogh $\rightarrow$ Kandinsky',
                                  r'Kandinsky $\rightarrow$ Matisse',
                                  r'Matisse $\rightarrow$ Picasso',
                                  r'Picasso $\rightarrow$ Miro',
                                  r'Miro $\rightarrow$ Pollock'])
fig.autofmt_xdate()
#ax.set_yticklabels([])
plt.legend()
plt.savefig("caso3_oposEinov.png")

plt.clf()
ax = fig.add_subplot(111)
ax.plot(range(len(dialeticas)), dialeticas, label="Dialetica")
for i in range(len(dialeticas)):
    ax.text(i, dialeticas[i], '%.2f' % dialeticas[i], fontsize=11)

dialabels = [r'Caravaggio $\rightarrow$ Frans Hals $\rightarrow$ Poussin',
             r'Frans Hals $\rightarrow$ Poussin $\rightarrow$ Velazquez',
             r'Poussin $\rightarrow$ Velazquez $\rightarrow$ Rembrandt',
             r'Velazquez $\rightarrow$ Rembrandt $\rightarrow$ Vermeer',
             r'Rembrandt $\rightarrow$ Vermeer $\rightarrow$ Van Gogh',
             r'Vermeer $\rightarrow$ Van Gogh $\rightarrow$ Kandinsky',
             r'Van Gogh $\rightarrow$ Kandinsky $\rightarrow$ Matisse',
             r'Kandinsky $\rightarrow$ Matisse $\rightarrow$ Picasso',
             r'Matisse $\rightarrow$ Picasso $\rightarrow$ Miro',
             r'Picasso $\rightarrow$ Miro $\rightarrow$ Pollock']

plt.xticks(range(len(dialeticas)), dialabels)
fig.autofmt_xdate()
plt.legend()
plt.savefig("caso3_dialetica.png")

