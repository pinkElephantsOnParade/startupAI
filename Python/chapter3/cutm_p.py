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
	regexp = re.compile(r'^(?:\xe4[\xb8-\xbf][\x80-\xbf]|[\xe5-\xe9][\x80-\xbf][\x80-\xbf]|\xef\xa4\xa9|\xef\xa7\x9c|\xef\xa8[\x8e-\xad])+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	全角カタカナかそれ以外かの判別
"""
def isKatakana(word):
	regexp = re.compile(r'^(?:\xe3\x82[\xa1-\xbf]|\xe3\x83[\x80-\xb6]|\xe3\x83\xbc)+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	全角ひらがなかそれ以外かの判別
"""
def isHiragana(word):
	regexp = re.compile(r'^(?:\xE3\x81[\x81-\xBF]|\xE3\x82[\x80-\x93])+$')
	result = regexp.search(word.encode('utf-8'))
	if result != None :
		return True
	else :
		return False

"""
	区読点の判別
"""
def isPunct(word):
	if word == u"．" or word == u"。" or word == u"，" or word == u"、":
		return True
	else :
		return False

"""
	字種の設定
		漢字は０
		カタカナは１
		その他は２
"""
def typeset(word):
	if isKanji(word):
		return 0
	elif isKatakana(word):
		return 1
	else :
		return 2

"""
	形態素の切り出し
"""
def outputMorph(sentence):
	now = 0
	last = 0
	last = typeset(sentence[0])
	outputSent = ""
	for i,tango in enumerate(sentence):
		pass
		if isPunct(tango) :
			outputSent += u"\n"
			outputSent += tango
			outputSent += u"\n"
			if i < len(sentence) - 1:
				last = typeset(sentence[i + 1]) 
		else :
			now = typeset(sentence[i])
			if now != last:
				outputSent += u"\n"
				last = now
			outputSent += tango

	return outputSent

if __name__ == "__main__":
	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath)]
	output = ""

	for lists in textList:
		if len(lists) != 0:
			output += outputMorph(lists)

	print output
