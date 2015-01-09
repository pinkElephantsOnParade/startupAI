#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import re
import sys
import codecs
from collections import Counter

"""
	コマンドラインから文字列を抽出する
	.txt以外は強制終了
"""
def getTextPathInCommandLine():
	argvs = sys.argv  # コマンドライン引数を格納したリストの取得
	argc = len(argvs) # 引数の個数


	if argc != 2:   # 引数が２つじゃない場合は、その旨を表示
	    print 'Usage: # python %s filepath' % argvs[0]
	    quit()         # プログラムの終了
	else :
		root, ext = os.path.splitext(argvs[1])
		if ext != '.txt':
			print 'Usage: # %s is not text file. You should change into the ext of text.' % argvs[1]
			quit()


	return argvs[1]

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
	テキストファイルのフォーマットチェック
"""
def fileFormatCheck(textList):
	if len(textList) == 0:
		print 'Usage: #0 This text format is incorrect.'
		quit()

	initTxtLength = len(textList[0].strip())

	for lists in textList:
		if len(lists.strip()) != 0:
			if initTxtLength != len(lists.strip()):
				print 'Usage: #1 This text format is incorrect.'
				quit()

"""
	要素数をカウントするリストを生成
"""
def makeListInElementCount(objList):
	uniqueList = list(set(objList))
	numList = []
	countDic = {}

	for lists in uniqueList:
		countDic[lists] = objList.count(lists)
#		numList.append(objList.count(lists))

#	return [uniqueList, numList]
	return sorted(countDic.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath)]
	fileFormatCheck(textList)
	countList = []

	#python2.7以前の場合
	if sys.version_info[1] < 7:
		countList = makeListInElementCount(textList)
	else:
		countList = sorted(Counter(textList).items(), key=lambda x: x[1], reverse=True)

	for lines in countList:
		print lines[0] + " "+ str(lines[1])
