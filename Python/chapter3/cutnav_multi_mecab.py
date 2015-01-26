#!/usr/bin/python
# -*- coding: utf-8 -*-


import MeCab
import sys
import string
import os.path
import codecs
from collections import Counter

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
		dicPathInfo[argvs[1]] = 0
	elif argc == 3:
		dicPathInfo[argvs[1]] = checkOptionCommand(argvs[2])
	else:
	    print 'Usage: # [python file(.py)][input folder][option command]'
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
	テキストファイルに書き込む
"""
def setWriteLineList(name,outstr):
	fout = codecs.open(name + '.txt', 'a', 'utf-8')
#	fout = codecs.open(name + '.txt', 'a')
	fout.write(outstr) # 引数の文字列をファイルに書き込む
	fout.close() # ファイルを閉じる


"""
	品詞の切り出し
"""
def outputPart(lists, option):
	partList = ""
	partKind = ""
	outputList = []

	if txtPath.values()[0] == 0:
		partKind = u"名詞"
	elif txtPath.values()[0] == 1:
		partKind = u"動詞"
	elif txtPath.values()[0] == 2:
		partKind = u"形容詞"
	elif txtPath.values()[0] == 3:
		partKind = u"形容動詞"
	else :
		partKind = u"名詞"

	try:
		t = MeCab.Tagger (" ".join(sys.argv))
		for sentence in lists:
			m = t.parseToNode(sentence.encode(sys.stdout.encoding))
			while m:
				if m.feature.split(',')[0].decode('utf-8') == partKind:
					outputList.append(m.feature.split(',')[6].decode('utf-8'))
				m = m.next

		return sorted(Counter(outputList).items(), key=lambda x: x[1], reverse=True)

	except RuntimeError, e:
	    print "RuntimeError:", e

def selectPartName(value):
	name = ""
	if value == 0:
		name = u"noun"
	elif value == 1:
		name = u"verb"
	elif value == 2:
		name = u"adj"
	elif value == 3:
		name = u"adjv"
	else :
		name = u"noun"
	return name

#-----main-----
if __name__ == "__main__":
	textList = []
	outputList = []
	txtPath = getTextPathInCommandLine()
	if os.path.isdir(txtPath.keys()[0]):
		files = os.listdir(txtPath.keys()[0])
		for fileName in files:
			textList += [item.strip() for item in getReadLineList(txtPath.keys()[0] + fileName)]
#		print txtPath.keys()[0]
#		textList = [item.strip() for item in getReadLineList(txtPath.keys()[0])]
		outputList += outputPart(textList, txtPath.values()[0])
		for item in outputList:
			print item[0] + u' ' + str(item[1]) 
#			setWriteLineList("out_noun", item)

	else :
		print txtPath.keys()[0] + "doesn't directory."



'''
		textName = selectPartName(txtPath.values()[0])
		outputList = outputPart(textList, txtPath.values()[0])

		for item in outputList:
			setWriteLineList(textName, item[0] + '\n')
'''

