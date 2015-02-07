#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
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
	全ての単語が既に使われているかチェック
'''
def lowerAllFlagWord(lists):
	lowerFlag = True
	for item in lists:
		if item[0]:
			lowerFlag = False
	return lowerFlag

'''
	対象リストから単語を選択
'''
def pickupWord(lists):
	pWord = ""
	maxCount = 0

	while maxCount < 1000:
		randIndex = random.randint(0, len(lists) -1)
		if lists[randIndex][0]:
			lists[randIndex][0] = False
			pWord = lists[randIndex][1]
			break
		maxCount += 1

	return pWord


'''
	意味ネットワークの探索
'''
def searchword(dic, word):
	SvsC = []
	if dic.has_key(word) and lowerAllFlagWord(dic[word]) == False:
		SvsC.append(word)
		SvsC.append(pickupWord(dic[word]))
	return SvsC


'''
	連想の処理
'''
def searchsnet(dic, word):

	keyword = word
	while 1: 
		svsc = searchword(dic, keyword)
		if len(svsc) == 2:
			print svsc[0] + u"は" + svsc[1]
			keyword = svsc[1]
		else :
			print keyword + u"は・・・わからない！"
			break
		
if __name__ == "__main__":
	textList = [item.strip() for item in getReadLineList("kk.txt")]
#	dicISA = makeIsAData(textList)
	print str(len(textList)) + u"個の意味ネットワークを読み込みました"
	print u"連想を開始する単語を入力してください．"
	commandLine = raw_input("単語(qで終了)：")	
	while 1:
		if commandLine == "q":
			break
		else:
			searchsnet(makeIsAData(textList), commandLine.decode('utf-8'))
			print u"連想を開始する次の単語を入力してください．"
			commandLine = raw_input("単語(qで終了)：")

	print u"処理を終わります．"