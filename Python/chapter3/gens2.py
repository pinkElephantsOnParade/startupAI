#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
	書き換え規則による文の生成プログラムその2
	書き換え規則Bに従って文を生成します
	書き換え規則B
		規則①	<文>→<名詞句＞＜動詞句＞
		規則②	<名詞句>→＜形容詞句＞＜名詞＞は
		規則③	<名詞句>→＜名詞＞は
		規則④	<動詞句>→＜動詞＞
		規則⑤	<動詞句>→＜形容詞＞
		規則⑥	<動詞句>→＜形容動詞＞
		規則⑦	<形容詞句>→＜形容詞＞＜形容詞句＞
		規則⑧	<形容詞句>→＜形容詞＞

	注意
		同一フォルダ配下に
			noun.txt
			verb.txt
			adj.txt
			adjv.txt
		は必要です

'''
import sys
import string
import os.path
import codecs
import random


"""
	読み込んだテキストファイルを改行単位にリスト化する
"""
def getReadLineList(path):

	if os.path.isfile(path) == False:
		print 'Usage: # %s does not exist.' % path
		quit()
	else :
		iStream = codecs.open(path, 'r', 'utf-8')
		lineList = iStream.readlines()
		iStream.close()
	return lineList

"""
	動詞句生成
		規則④	<動詞句>→＜動詞＞
		規則⑤	<動詞句>→＜形容詞＞
		規則⑥	<動詞句>→＜形容動詞＞
"""
def vp(vlist, alist, dlist):
	dice = random.randint(1,3)
	if dice == 1:
		return random.choice(vlist)
	elif dice == 2:
		return random.choice(alist)
	elif dice == 3:
		return random.choice(dlist)
	else :
		return random.choice(vlist)

"""
	形容詞句生成
		規則⑦	<形容詞句>→＜形容詞＞＜形容詞句＞
		規則⑧	<形容詞句>→＜形容詞＞
"""
def ap(alist):
	dice = random.randint(1,2) 
	if dice == 1:
		return ap(alist) + random.choice(alist)
	else :
		return random.choice(alist)

"""
	名詞句生成
		規則②	<名詞句>→＜形容詞句＞＜名詞＞は
		規則③	<名詞句>→＜名詞＞は
"""
def np(nlist, alist):
	dice = random.randint(1,2) 
	if dice == 1:
		return ap(alist) + random.choice(nlist) + u"は"		
	else :
		return random.choice(nlist) + u"は"

"""
	文章生成
		規則①	<文>→<名詞句＞＜動詞句＞
"""
def makeSentence(nlist, vlist, alist, dlist):
	return np(nlist, alist) + vp(vlist, alist, dlist)

#-----main-----
if __name__ == "__main__":
	nounList = [item.strip() for item in getReadLineList("noun.txt")]
	verbList = [item.strip() for item in getReadLineList("verb.txt")]
	adjList = [item.strip() for item in getReadLineList("adj.txt")]
	adjvList = [item.strip() for item in getReadLineList("adjv.txt")]

	for item in range(0, 50):
		print makeSentence(nounList, verbList, adjList, adjvList)
