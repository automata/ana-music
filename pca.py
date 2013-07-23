# -*- coding: utf-8 -*-

### Principal Component Analysis
###
### Author: Vilson Vieira <vilson@void.cc>
###         University of São Paulo (USP) / IFSC @ 2012

import numpy as n

## para retirar o warning quando converte array de complexos para reais
import warnings
warnings.simplefilter("ignore", n.ComplexWarning)

def pca(data):
   data = n.array(data, dtype=float)

   # normalizamos a matriz de dados (X = X - mean) e dividimos pelo d.p.
   #     X = (X - mean) / dp
   for i in xrange(data.shape[1]):
      # adiciono um valor irrisorio 0.001 no denominador para nao
      # dar divisao por zero
      data[:,i] = (data[:,i] - data[:,i].mean())/(data[:,i].std()+0.001)

   # calculamos a matriz de covariância de X
   matriz_cov = n.cov(data, bias=1, rowvar=0)

   # calculamos os autovetores e autovalores e ordenamos em ordem decresc.
   autovalores, autovetores = n.linalg.eig(matriz_cov)
   args = n.argsort(autovalores)[::-1]
   autovalores = autovalores[args]
   autovetores = autovetores[args]

   # calculamos os componentes principais para todos os dados
   dados_finais = n.dot(autovetores.T, data.T)
   principais = dados_finais.T

   return principais

def pca_autoval(data):
   """
   Retorna componentes principais, autovalores e contribuição de cada
   componente (proporção dos autovalores).
   """
   data = n.array(data, dtype=float)

   # normalizamos a matriz de dados (X = X - mean) e dividimos pelo d.p.
   #     X = (X - mean) / dp
   for i in xrange(data.shape[1]):
      # adiciono um valor irrisorio 0.001 no denominador para nao
      # dar divisao por zero
      data[:,i] = (data[:,i] - data[:,i].mean())/(data[:,i].std()+0.001)

   # calculamos a matriz de covariância de X
   matriz_cov = n.cov(data, bias=1, rowvar=0)

   # calculamos os autovetores e autovalores e ordenamos em ordem decresc.
   autovalores, autovetores = n.linalg.eig(matriz_cov)
   autovalores_desord = autovalores.copy()
   args = n.argsort(autovalores)[::-1]
   autovalores = autovalores[args]
   autovetores = autovetores[args]

   # calculamos os componentes principais para todos os dados
   dados_finais = n.dot(autovetores.T, data.T)
   principais = dados_finais.T

   # proporção dos autovalores
   autovalores_prop = autovalores / n.sum(autovalores)

   return principais, autovalores_desord / n.sum(autovalores), autovalores_prop, args


def norm(data):
   data = n.array(data, dtype=float)

   # normalizamos a matriz de dados (X = X - mean) e dividimos pelo d.p.
   #     X = (X - mean) / dp
   for i in xrange(data.shape[1]):
      # adiciono um valor irrisorio 0.001 no denominador para nao
      # dar divisao por zero
      data[:,i] = (data[:,i] - data[:,i].mean())/(data[:,i].std()+0.001)

   return data
