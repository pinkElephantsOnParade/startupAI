#!/usr/bin/python
# -*- coding: utf-8 -*-

# 強化学習によるじゃんけんエージェントプログラム(環境つき）agent.c
# このプログラムは，じゃんけんエージェントと環境の両方の機能を果たします
# 実行するには，環境がエージェントに与える手の系列を格納したファイルhands.txtが必要です
# agentプログラムがおかれたディレクトリには，内部状態の途中経過を保存するファイルint.txtが作成されます

import sys
import os.path
import codecs
import re
import random

#INPUTFILENAME = "hands.txt"	# グーチョキパーパーチョキグー  の繰り返し　
#INPUTFILENAME = "hands1.txt"	# グーチョキパー  の繰り返し
INPUTFILENAME = "hands2.txt"	# グーチョキパー　途中で　パーチョキグー
OUTPUTFILENAME = "int.txt" 
INITVAL = 10

GU = 0    #グー
CYOKI = 1 #チョキ
PA = 2   #パー

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
	fout = codecs.open(OUTPUTFILENAME, 'a', 'utf-8')
	fout.write(outstr) # 引数の文字列をファイルに書き込む
	fout.close() # ファイルを閉じる


"""
	報酬の設定
"""
def setReward(oppHand, myHand):
	rtable=[[0,-1,1],[1,0,-1],[-1,1,0]] 
	return rtable[oppHand][myHand]

"""
	学習
"""
def learning(reward, oppHand, myHand, qTable):
	alpha = 0
	for i in xrange(3):
		if i == myHand: alpha = 1
		else: alpha = -1

		#報酬に基づいてqを更新
		#出した手が正の報酬のとき　
		#   出した手(+)
		#   それ以外の手(-)
		if 0 < qTable[oppHand][i] + alpha * reward:
			qTable[oppHand][i] += alpha*reward

	#ファイルへの内部状態の書き出し
	printStr = ""
	for row in qTable:
		for col in row:
			printStr += str(col) + u" "
	printStr += u"\n"
	setWriteLineList(printStr)

"""
	行動選択（手の決定）
"""
def selectaction(oppHand, qTable):
	sumVal = qTable[oppHand][0] + qTable[oppHand][1] + qTable[oppHand][2]
	step = 0 
	acc = 0
	point = 0

	step = random.randint(0, sumVal)
	while acc <= step:
		if 2 < point: break
		acc += qTable[oppHand][point]
		point += 1

	return point - 1

if __name__ == "__main__":
	#Q学習用のテーブル
	q = [[INITVAL,INITVAL,INITVAL],
		[INITVAL,INITVAL,INITVAL],
		[INITVAL,INITVAL,INITVAL]]
	myHand = GU
	lastOppositeHand = GU
	reward = 0
	printStr = ""
	#相手の手
	handsList = [int(item.strip()) for item in getReadLineList(INPUTFILENAME)]

	for oppositeHand in handsList:
		printStr = ""
		reward = setReward(oppositeHand, myHand)
		if reward != 0:
			#報酬に基づく学習
			learning(reward, lastOppositeHand, myHand, q) 
		printStr = str(oppositeHand) + u" " + str(myHand) + u" "
		#次の行動を決定する
		myHand = selectaction(oppositeHand, q)
		print printStr + str(myHand)
		lastOppositeHand = oppositeHand
