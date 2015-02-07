#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re

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
	is-aデータを作る
"""
def makeIsAData(tangoList):
	dicIsa = {}
	odd = True
	keyItem = ""
	flag = True
	for item in tangoList:
		if odd:
			keyItem = item
			odd = False
		else :
			if dicIsa.has_key(keyItem):
				for dicItem	in dicIsa[keyItem]: 							
					if dicItem[1] == item:
						flag = False			
				if flag:
					dicIsa[keyItem].append([True, item])
				else :
					flag = True
			else :
				dicIsa[keyItem] = [[True, item]]
			odd = True
	return dicIsa

'''
	意味ネットワークの探索
'''
def searchword(dic, word):
	if dic.has_key(word):
		for item in dic[word]:
			print item[1]
	else :
		print u"ないお。。。"

'''
	連想の処理
'''
def searchsnet(dic, word):
	searchword(dic, word)

		
if __name__ == "__main__":
	textList = [item.strip() for item in getReadLineList("kk.txt")]

	print str(len(textList)) + u"個の意味ネットワークを読み込みました"
	print u"連想を開始する単語を入力してください．"
	commandLine = raw_input("単語：")	
	while 1:
		if commandLine == "q":
			break
		else:
			searchsnet(makeIsAData(textList), commandLine.decode('utf-8'))
			print u"連想を開始する次の単語を入力してください．"
			commandLine = raw_input("単語：")

	print u"処理を終わります．"