# Análise de Compositores

Começando a fazer para música o que fizemos para pinturas. Iniciando com corpus
que temos de Beethoven, Mozart e Scarlatti. Incluir em seguida Bach e talvez
arquivos MIDI das sonatas de Scarlatti.

# Primeira fase: Sonatas

Antes de tudo, instale Python, Numpy, Pylab, Music21 e scikit-learn:

    sudo apt-get install python python-numpy python-pylab python-setuptools
    sudo easy_install music21
    sudo easy_install scikit-learn

Para extrair as features de corpus/corpus_{scarlatti,haydn,beethoven,mozart}/

    python primeira_fase.py
    
Irá gerar arquivos com features calculadas em tmp/. Para analisar:

    python primeira_fase_ana.py
    
Irá gerar os resultados em g1.png (gráfico de sério temporal dos compositores).

    eog g1.png

# Classical

## Corpus

### Primeira fase: Piano Sonatas

* 32 Sonatas by Beethoven (102 movements)
* 59 Sonatas by Scarlatti
* 17 Sonatas by Mozart (51 movements)
* Haydn Piano Sonatas (17 movements) 

* Incluir Keyboard music em MuseData (Bach, Vivaldi, ...)

Resultados em primeira_fase/

### Segunda fase: Forma Sonata

Todos os kerns em http://kern.humdrum.org/search?s=t&keyword=sonata

### Terceira fase: Todos, classificados em movimentos

Todos os arquivos kern em corpus/classical/corpus_classical.txt, separar
em classes segundo http://kern.ccarh.org/cgi-bin/browse?l=/users/craig/classical
Talvez também incluir:

* 9 Sinfonias de Beethoven: http://www.musedata.org/encodings/beet/bh/
* Piano concerto nr 2
* Violin concerto
* Keyboard music de Bach: http://www.musedata.org/encodings/bach/
* Concertos e outras obras de Vivaldi, Haydn, Handel, Telemann, Dvorák disponíveis em http://www.musedata.org/

## Features

Usamos features provenientes do music21 (native e jSymbolic). Ao total são 91
feature extractors, gerando um total de 633 medidas. As feature extractors estão
listadas em https://gist.github.com/automata/5872349 e descritas em detalhes em:
* native: http://web.mit.edu/music21/doc/html/moduleFeaturesNative.html
* jSymbolic: http://jmir.sourceforge.net/jSymbolic.html

# MPB

## Corpus

* Noel Rosa
* Tom Jobim
* Chico Buarque
* Caetano Veloso
    * http://www.musicaudio.xpg.com.br/midi/c.htm
* Roberto Carlos
* Djavan
* Lenine

## Features

Mesmas que para clássico??

# Notas

corpus/ possui todos os arquivos hundrum usados. em corpus/classical há
*todos* os arquivos do repositório hundrum!

old/ possui arquivos para referência, de experimentos passados.

primeira_fase_resultados/ os scripts e resultados da primeira fase (cópia)

tmp/ os arquivos csv temporários

util/ script para fazer download do kern.hundrum... melhorar...

# Referências

* Sobre extração de features usando music21:
  http://ismir2011.ismir.net/papers/PS3-6.pdf
