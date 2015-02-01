#!/usr/bin/python
# -*- coding: utf-8 -*-

import MeCab
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
	文章から名詞を取得
"""
def getNoun(sentence):
	inputWordList = []
	partKind = u"名詞"

	try :
		t = MeCab.Tagger (" ".join(sys.argv))
		m = t.parseToNode(sentence.encode(sys.stdout.encoding))
		while m:
			if len(m.surface.strip()) != 0:
				if m.feature.split(',')[0].decode('utf-8') == partKind:
					inputWordList.append(m.surface) 
			m = m.next

		return inputWordList
	except RuntimeError, e:
	    print "RuntimeError:", e

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


#-----無愛想なchatbot-----
def communication(plists):
  while 1:
    commandLine = raw_input("あなた：")
    if commandLine == "q":
        break
    else:
    	if isZenkaku(commandLine.strip().decode('utf-8')) == False:
    		print u"さくら：文字化けしているお(* ´Д`) 全角で話してほしいお(￣ー￣)"
    	else :
	    	sentence = commandLine.strip().decode('utf-8')
	    	nounList = getNoun(commandLine.decode('utf-8'))
	    	if len(nounList) == 0:
	    		keyword = u"人工知能"
	    	else:
		    	keyword = random.choice(nounList).decode('utf-8')
	    	print u"さくら：" + generates(keyword, plists)

if __name__ == "__main__":

	textList = [item.strip() for item in getReadLineList(u"morph.txt")]
	pairMorph = morphFormat(textList)

	print "さくら：メッセージをどうぞ('q'で終了)"
	communication(pairMorph)
	print "さくら：ばいば～い"
