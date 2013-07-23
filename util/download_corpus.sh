#!/bin/bash

# Piano Sonatas

# Haydn
mkdir corpus_haydn
cd corpus_haydn
wget 'http://kern.ccarh.org/cgi-bin/ksdata?l=users/craig/classical/haydn/keyboard/uesonatas&format=zip' -O foo.zip
unzip foo.zip
mv uesonatas/* ./
rm -rf uesonatas *.zip



