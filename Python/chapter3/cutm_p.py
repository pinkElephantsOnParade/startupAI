#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re

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
	全角判定
"""
def isZenkaku(sentence):
	bFlag = True
	regexp = re.compile('(?:\xEF\xBD[\xA1-\xBF]|\xEF\xBE[\x80-\x9F])|[\x20-\x7E]')
	result = regexp.search(sentence)
	if result != None :
		bFlag = False
	else :
		bFlag = True
	return bFlag

"""
	漢字かそれ以外かの判別
"""
def isKanji(word):


"""
	カタカナかそれ以外かの判別
"""
def isKatakana(word):



"""
	字種の設定
		漢字は０
		カタカナは１
		その他は２
"""
def typeset(word):
	if isKanji(word):			return 0
	else if isKatakana(word):	return 1
	else :						return 2

"""
	形態素の切り出し
"""
def outputMorph(sentence):
	now = 0
	last = 0
	last = typeset(sentence[0])

if __name__ == "__main__":
	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath)]

	for lists in textList:
		if len(lists) != 0:
			outputMorph(lists)
