# encoding: utf-8

# CASO 3: LDA usado para classificar

# 1. normalizo F
# 2. separo as pinturas em 12 classes
# 3. calculo LDA
# 4. calculo os protótipos a partir do LDA (Prots)
# 5. calculo dialética, inovação e oposição dos Prots

import pickle as pk
import numpy as np
import pca as pc
import pylab as py
import itertools
import matplotlib.pyplot as plt
import matplotlib.image as image

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
# cols = [2,3]
# F__ = T[:,cols]
F__ = T

# normalizamos
M = np.mean(F__, axis=0)
D = np.std(F__, axis=0)
F = np.nan_to_num((F__-M) / D)

# PCA


dados = F
ncomp = 4
ncarac = 2

# calculamos a matriz de covariância de X
matriz_cov = np.cov(dados, bias=1, rowvar=0)
print '\n*** Matriz de covariância:\n', np.around(matriz_cov, decimals=2)

# calculamos a correlação de pearson para todas as notas
stds=np.std(dados, 0)
pearson=np.zeros((ncarac,ncarac))
for i in xrange(ncarac):
   for j in xrange(ncarac):
     pearson[i,j]=matriz_cov[i,j]/(stds[i]*stds[j])

print '\n*** Pearson (igual matriz covar.):\n ###TABLE III. Pearson correlation coefficients between the eight musical characteristics.'
for linha in pearson:
    print [str(round(x, ndigits=2)) for x in linha]

# calculamos os autovetores e autovalores e ordenamos em ordem decresc.
autovalores, autovetores = np.linalg.eig(matriz_cov)
args = np.argsort(autovalores)[::-1]
autovalores = autovalores[args]
autovetores = autovetores[args]
# autovalores (var.) como porcentagem dos autovalores
autovalores_prop = [av/np.sum(autovalores) for av in autovalores]

# calculamos os componentes principais para todos os dados
dados_finais = np.dot(autovetores.T, dados.T)
principais = dados_finais.T[:,:2] # apenas 2 primeiros componentes

princ_orig = principais 

print 'COMPONENTES', principais
print 'INDICE COMPONENTES', args
print 'CONTRIBUICAO', autovalores_prop

# separamos as pinturas em classes de 20 pinturas, uma para cada pintor
# e calculamos os protótipos (pontos médios)
Fs = []
Prots = []
for i in range(0,240,20):
    Fs.append(principais[i:i+20])
    prot = np.array([np.mean(principais[i:i+20, k]) for
                     k in range(princ_orig.shape[1])])
    #prot = np.array([np.mean(X_r2[y==i, k]) for k in range(X_r2.shape[1])])
    #prot = np.nan_to_num(prot)
    Prots.append(prot)

agents = compositores

# ordenamos a tabela pela ordem correta cronológica dos pintores
Ford = Fs
principais = np.array(Ford)

annotate_xy = [(-70,-50), (20,-50), (90,-40), (-50,-55), (110,-20), (-50,10),
               (15,50), (-60,30), (-100,-50), (-30,70), (-40,40), (-80,40)]

plt.figure(figsize=(12,12))
ax = plt.subplot(111)
for i in range(ncomp):
    x = -Prots[i][1]
    y = Prots[i][0]
    aaf = np.sum(Prots[:i+1], 0) / (i+1)
    ax.plot(-aaf[1], aaf[0], 'o', color="#666666")
    if i != 0:
        ax.plot((-aat[1], -aaf[1]), (aat[0], aaf[0]), ':', color='#333333')
    aat = np.copy(aaf)
    ax.plot(x, y, 'bo')
    #ax.text(x, y, str(i+1) + ': ' + conf.artistas[conf.ordem[i]], fontsize=11)

    ax.annotate(str(i+1) + ': ' + agents[i], xy=(x,y), xytext=annotate_xy[i], 
                textcoords='offset points', ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3,rad=0.1',
                                color='red'), fontsize=14)


    # plotamos também as pinturas todas
    ax.plot(-Ford[i][:,1], Ford[i][:,0], 'o',
            label=str(i+1) + ': ' + agents[i],
            color=py.cm.jet(np.float(i) / (len(Ford)+1)), alpha=.4)
    # plotamos o protótipo (ponto médio)
    ax.plot(-Prots[i][1], Prots[i][0], 'k+')
Prots = np.array(Prots)
ax.plot(-Prots[:,1], Prots[:,0], c='#000000')
plt.legend(loc='upper left')
plt.ylabel('First Component')
plt.xlabel('Second Component')
#plt.title('LDA')
plt.savefig('scar_pca_g1.pdf', bbox_inches='tight')

# dados usados para cálculo dos 'metrics'
agents = compositores
dados = np.array(Prots)
ncomp = 4
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
ax.plot(range(len(oposicao)), oposicao, label="Opposition")
for i in range(len(oposicao)):
    ax.text(i, oposicao[i], '%.2f' % oposicao[i], fontsize=11)
ax.plot(range(len(inovacao)), inovacao, label="Skewness")
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
plt.savefig("scar_pca_oposEinov.pdf", bbox_inches='tight')

plt.clf()
ax = fig.add_subplot(111)
ax.plot(range(len(dialeticas)), dialeticas, label="Counter-dialectics")
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
plt.savefig("scar_pca_dialetica.pdf", bbox_inches='tight')

# #
# # Perturbação
# #

# nperturb = 1000
# # distancias[original, ruido, amostra]
# distancias = np.zeros((ncomp, ncomp, nperturb))
# autovals = np.zeros((nperturb, 2))  # agora para 8d
# princ_orig = princ_orig[:,:2]
# #princ = princ[:,:2]

# for foobar in xrange(nperturb):
#     dist = np.random.randint(-2, 3, copia_dados.shape)
#     copia_dados += dist

#     for i in xrange(copia_dados.shape[1]):
#         copia_dados[:,i] = (copia_dados[:,i] - copia_dados[:,i].mean())/copia_dados[:,i].std()

#     # fazemos pca para dados considerando esses pontos aleatórios entre -2 e 2
#     # FIXME: substituir depois pca_nipals
#     T, P, E = pca.PCA_nipals(copia_dados)
#     autovals[foobar] = E[:2]
#     princ = T[:,:2]
#     for i in xrange(ncomp):
#         for j in xrange(ncomp):
#             distancias[i, j, foobar] = np.sum((princ_orig[i] - princ[j])**2)**.5

# stds = np.zeros((ncomp, ncomp))
# means = np.zeros((ncomp, ncomp))
# main_stds = []
# main_means = []
# print 'dados', copia_dados
# for i in xrange(ncomp):
#     for j in xrange(ncomp):
#         stds[i,j] = distancias[i,j,:].std()
#         means[i,j] = distancias[i,j,:].mean()
#         if i == j:
#           main_stds.append(stds[i,j])
#           main_means.append(means[i,j])
# np.savetxt("mean2_.txt",means,"%.2e")
# np.savetxt("stds2_.txt",stds,"%.2e")

# print '###TABLE V.### Average and standard deviation of the deviations for each composer and for the 8 eigenvalues.'

# print 'main_means', main_means
# print 'main_stds', main_stds

# # Cálculo das médias e variâncias dos desvios dos primeiros 4 autovalores

# deltas = autovals - autovalores_prop[:8]
# medias = deltas.mean(0)
# desvios = deltas.std(0)
# print 'eigenvalues means', medias
# print 'eigenvalues stds', desvios

