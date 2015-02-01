#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
import random

"""
	拡張子.txtチェック
"""
def checkExeTxt(path):
	root, ext = os.path.splitext(path)	
	if ext == '.txt':
		return True
	else :
		return False

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
	形態素ファイルの読み込み
"""
def morphFormat(tList):
	pair = []
	prevItem = ""
	for i,item in enumerate(tList):
		if i == 0:
			prevItem = item
		else :
			pair.append([prevItem, item])
			prevItem = item
	return pair

"""
	開始文字が何回含まれるか数える
"""
def countFindFrontChar(word, lists):
	count = 0
	for element in lists:
		if word == element[0]:
			count = count + 1
	return count

"""
	先頭文字が合致する要素をリスト化する
"""
def extractElementListFromFrontWord(word, lists):
	extList = []
	for element in lists:
		if word == element[0]:
			extList.append(element)
	return extList

"""
	次の一文字をランダムに選択する
"""
def setnext(word, glist):
	resultList = extractElementListFromFrontWord(word, glist)
	randIndex = 0
	nextWord = ""
	if len(resultList) == 0:
		randIndex = random.randint(0, len(glist) - 1)
		nextWord = glist[randIndex][1]
	else :
		randIndex = random.randint(0, len(resultList) - 1)
		nextWord = resultList[randIndex][1]

	return nextWord

"""
	文の生成
"""
def generates(keyword, glist):

	#先頭１文字を挿入
	botSentence = keyword
	nextWord = keyword

	#2文字目以降を挿入
	while nextWord != u"．" and nextWord != u"。":
		nextWord = setnext(nextWord, glist)
		botSentence = botSentence + nextWord
	return botSentence


if __name__ == "__main__":
	keyword = raw_input("開始文字列：")
	textList = [item.strip() for item in getReadLineList(u"morph.txt")]
	pairMorph = morphFormat(textList)

	for item in range(0,10):
		print generates(keyword.decode('utf-8'), pairMorph)
	