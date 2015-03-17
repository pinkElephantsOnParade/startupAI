#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
import random

FILENAME = u"morph.txt"

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
	テキストファイルに書き込む
"""
def setWriteLineList(outstr):
	fout = codecs.open(FILENAME, 'a', 'utf-8')
	fout.write(outstr) # 引数の文字列をファイルに書き込む
	fout.close() # ファイルを閉じる

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

"""
	開始文字列の決定
"""
def setstartch(sentence):
	exKanji = ""
	i = 0

	for i, word in enumerate(sentence):
		if isKanji(word):
			break

	if i == len(sentence) - 1 and isKanji(sentence[i]) == False:
		exKanji = u"人工知能"
	else :
		while isKanji(sentence[i]) and sentence[i] != u"\n":
			exKanji = exKanji + sentence[i]
			i = i + 1
			if i == len(sentence) :
				break
	return exKanji

"""
	利用者の入力から形態素ファイルを更新する
"""
def addmorth(sentence):
	setWriteLineList(outputMorph(sentence))

#-----無愛想なchatbot-----
def communication():
	textList = []
	while 1:
		commandLine = raw_input("あなた：")
		if commandLine == "q":
			break
		else:
			if isZenkaku(commandLine.strip().decode('utf-8')) == False:
				print u"さくら：文字化けしているお(* ´Д`) 全角で話してほしいお(￣ー￣)"
			else :
				sentence = commandLine.strip().decode('utf-8')
				#相手の会話を形態素分割し、テキストに保存
				addmorth(sentence) 

				#形態素データを参照し、形態素の連鎖配列を作成
				textList = [item.strip() for item in getReadLineList(FILENAME)]
				pairMorph = morphFormat(textList)
				print u"さくら：" + generates(setstartch(sentence), pairMorph)


if __name__ == "__main__":
	print "さくら：メッセージをどうぞ('q'で終了)"
	communication()
	print "さくら：ばいば～い"
	