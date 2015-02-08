#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
import random

'''
class rule:
	def __init__(self, word1, word2, word3, word4, word5, action):
		self.word1 = word1
		self.word2 = word2
		self.word3 = word3
		self.word4 = word4
		self.word5 = word5
		self.action = action

	def getWord1(self):
		return self.word1
	def getWord2(self):
		return self.word2
	def getWord3(self):
		return self.word3
	def getWord4(self):
		return self.word4
	def getWord5(self):
		return self.word5
	def getAction(self):
		return self.action
'''

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
	ルールを読み込む
"""
def readRule(lists):
	ruleList = []
	for lineItem in lists:
		ruleList.append(lineItem.split(u" "))
	return ruleList

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
	応答文の生成
"""
def answer(rList, sentence):
	matchIndexList = []
	count = 0
	max_count = 0
	max_index = []
	response = ""
	for i,items in enumerate(rList):
		for idx, unitItem in enumerate(items):
			if idx != 4 and unitItem in sentence and unitItem != u"-":
				count += 1
		if 0 < count: 
			matchIndexList.append([i, count])
			count = 0

	#言葉を選ぶ
	if 0 < len(matchIndexList):
		#頻出するキーワードの最大数をカウントする
		for idxItem in matchIndexList:
			if max_count < idxItem[1]:
				max_count = idxItem[1]
		#最大数カウントのルールを抽出
		for idxItem in matchIndexList:
			if max_count == idxItem[1]:
				max_index.append(idxItem[0])
		response = rList[max_index[random.randint(0, len(max_index) - 1)]][4]
	else :
		response = u"どうぞ続けてください"
	return response


#-----無愛想なchatbot-----
def communication(rList):

	while 1:
	    commandLine = raw_input("あなた：")
	    if commandLine == "q":
	    	break
	    else:
	    	if isZenkaku(commandLine.strip().decode('utf-8')) == False:
	    		print u"さくら：文字化けしているお(* ´Д`) 全角で話してほしいお(￣ー￣)"
	    	else :
		    	sentence = commandLine.strip().decode('utf-8')
		    	print answer(rList, sentence)
#		    	print u"さくら：" + answer(rList, sentence)



if __name__ == "__main__":
	textList = [item.strip() for item in getReadLineList(u"rule.txt")]
	ruleList = readRule(textList)

	print "さくら：さて，どうしました？('q'で終了)"
	communication(ruleList)
	print "さくら：それではお話を終わりましょう"	