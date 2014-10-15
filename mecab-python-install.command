#!/bin/sh

#install mecab
cd ~/Downloads/
curl -O https://mecab.googlecode.com/files/mecab-0.996.tar.gz
tar zxfv mecab-0.996.tar.gz
cd mecab-0.996
./configure
make
sudo make install


#install dictionary ipa
cd ~/Downloads/
curl -O https://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.tar.gz
tar zxfv mecab-ipadic-2.7.0-20070801.tar.gz
cd mecab-ipadic-2.7.0-20070801
./configure --with-charset=utf8
make
sudo make install


#install mecab python
cd ~/Downloads/
curl -O https://mecab.googlecode.com/files/mecab-python-0.996.tar.gz
tar zxfv mecab-python-0.996.tar.gz
cd mecab-python-0.996
python setup.py build
su
python setup.py install
