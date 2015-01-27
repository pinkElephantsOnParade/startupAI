#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
	書き換え規則　A
		規則①	<文>→<名詞句＞＜動詞句＞
		規則②	<名詞句>→＜名詞＞は
		規則③　 <動詞句>→＜動詞＞
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
	句生成
		規則②	<名詞句>→＜名詞＞は
"""
def np(nList):
	return random.choice(nList) + u"は"

"""
	句生成
		規則③　 <動詞句>→＜動詞＞
"""
def vp(vList):
	return random.choice(vList)


"""
	文章生成
		規則①	<文>→<名詞句＞＜動詞句＞
"""
def makeSentence(nList, vList):
	return np(nList) + vp(vList)	

#-----main-----
if __name__ == "__main__":
	nounList = [item.strip() for item in getReadLineList("noun.txt")]
	verbList = [item.strip() for item in getReadLineList("verb.txt")]

	for item in range(0, 50):
		print makeSentence(nounList, verbList)

#	print len(nounList)
#	print len(verbList)