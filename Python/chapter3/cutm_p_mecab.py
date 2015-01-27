#! /usr/bin/env python
# -*- coding:utf-8 -*-

import MeCab
import sys
import string
import os.path
import codecs

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
	テキストファイルに書き込む
"""
def setWriteLineList(name,outstr):
	fout = codecs.open(name + '.txt', 'a')
	fout.write(outstr + '\n') # 引数の文字列をファイルに書き込む
	fout.close() # ファイルを閉じる


#-----main-----
if __name__ == "__main__":

	txtPath = getTextPathInCommandLine()
	textList = [item.strip() for item in getReadLineList(txtPath)]
	fout = codecs.open('morph.txt', 'a')
	try:
		t = MeCab.Tagger (" ".join(sys.argv))
		for lists in textList:
			m = t.parseToNode(lists.encode('utf-8'))
			while m:
#				setWriteLineList("morph", m.surface)
#				fout.write(m.surface.decode('utf-8') + u'\n') # 引数の文字列をファイルに書き込む
				if len(m.surface.strip()) != 0:
					fout.write(m.surface + '\n') # 引数の文字列をファイルに書き込む
				m = m.next
		fout.close() # ファイルを閉じる
	except RuntimeError, e:
	    print "RuntimeError:", e

