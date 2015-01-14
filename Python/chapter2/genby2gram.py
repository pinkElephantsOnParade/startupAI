
# -*- coding: utf-8 -*-
import os.path
import re
import sys
import codecs
import random

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
	botSentence = ""
	nextWord = ""
	if len(keyword.strip()) != 3:
		print 'Usage: #2 Please input a 全角1文字.'
		quit()
	if len(keyword.strip().decode('utf-8')) != 1:
		print 'Usage: #2 Please input a 全角1文字.'
		quit()

#	chNumber = countFindFrontChar(keyword.strip().decode('utf-8'), glist)

	#先頭１文字を挿入
	botSentence = keyword.strip().decode('utf-8')
	nextWord = keyword.strip().decode('utf-8')
	maxCount = 0

	#2文字目以降を挿入
	while nextWord != "．".decode('utf-8') and nextWord != "。".decode('utf-8') and maxCount < 100:
		nextWord = setnext(nextWord, glist)
		botSentence = botSentence + nextWord
		maxCount += 1 		
	return botSentence

#-----main-----
if __name__ == "__main__":
	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath)]
	fileFormatCheck(textList)

	sentence = raw_input("開始文字を入力してください(全角１文字):")

	for i in range(10):
		print generates(sentence, textList)
