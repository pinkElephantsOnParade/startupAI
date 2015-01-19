#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re

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
	オプションチェック
	n(-n):名詞 				→	0
	v(-v):動詞 				→	1
	a(-a):形容詞 			→	2
	d(-d):形容動詞 			→	3
	それ以外のコマンドはエラー
"""
def checkOptionCommand(word):

	selection = 0

	if word == 'n' or word == 'v' or word == 'a' or word == 'd' or word == '-n' or word == '-v' or word == '-a' or word == '-d':
		if word == 'n' or word == '-n':
			selection = 0
		elif  word == 'v' or word == '-v':
			selection = 1
		elif  word == 'a' or word == '-a':
			selection = 2
		elif  word == 'd' or word == '-d':
			selection = 3
		else :
			selection = 0
	else :
		print 'Usage: # %s is not a option command.' % word
		quit()

	return selection


"""
	コマンドラインから文字列を抽出する
	.txt以外は強制終了
"""
def getTextPathInCommandLine():
	argvs = sys.argv  # コマンドライン引数を格納したリストの取得
	argc = len(argvs) # 引数の個数
	dicPathInfo = {}

	if argc == 2:
		if checkExeTxt(argvs[1]):
			dicPathInfo[argvs[1]] = 0
		else :
			print 'Usage: # %s is not text file. You should change into the ext of text.' % argvs[1]
			quit()
	elif argc == 3:
		if checkExeTxt(argvs[1]):
			dicPathInfo[argvs[1]] = checkOptionCommand(argvs[2])
		else :
			print 'Usage: # %s is not text file. You should change into the ext of text.' % argvs[1]
			quit()
	else:
	    print 'Usage: # python %s filepath' % argvs[0]
	    quit()         # プログラムの終了

	return dicPathInfo

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
	名詞の切り出し
"""
def outputNoun(sentence):
	now = 0
	last = 0
	last = typeset(sentence[0])
	outputSent = ""
	for i,tango in enumerate(sentence):
		now = typeset(sentence[i])
		if now != last and last == 0:
			outputSent += u"\n"
		if now == 0:
			outputSent += tango
		last = now
	return outputSent

"""
	動詞・形容詞・形容動詞の切り出し
	[漢字][漢字]...[指定したひらがな]
"""
def outputP(sentence, gobi):
	now = 2
	last = 2
	temp = ""
	k = ""

	for i, word in enumerate(sentence): 
		if i == 0:
			last = typeset(sentence[i])	
			if last == 0:
#				k += sentence[i]
				temp += sentence[i]			
		else :
			now = typeset(sentence[i])
			if now == 0:
				temp += sentence[i]
#				k += sentence[i]
			if now != last and last == 0:
				if sentence[i] == gobi:
					temp += sentence[i]
					k += temp
					k += u"\n"
				temp = ""
			last = now
			i += 1
	return k

if __name__ == "__main__":
	
	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath.keys()[0])]
	extractList = ""

	for sentence in textList:
		if txtPath.values()[0] == 0:
			extractList += outputNoun(sentence)
		elif txtPath.values()[0] == 1:
			extractList += outputP(sentence, u"う")
		elif txtPath.values()[0] == 2:
			extractList += outputP(sentence, u"い")
		elif txtPath.values()[0] == 3:
			extractList += outputP(sentence, u"だ")
		else :
			extractList += outputNoun(sentence)

	print extractList
