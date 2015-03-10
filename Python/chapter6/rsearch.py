#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import re
import random


POOLSIZE = 30  #プールサイズ
RULESIZE = 4  #遺伝子の持つルールの数
LOCUSSIZE = 4 #ひとつのルールが持つ遺伝子座の数

GMAX = 3 #打ち切り世代
MRATE = 0.5 #突然変異率

LOWERLIMIT = 0 #遺伝子を印字する最低適応度
MAXLINES = 64 #キーワードの組み合わせの最大数
LINESIZE = 64 #キーワードデータの行サイズ

"""
	遺伝子プールの初期化
"""
def initgene():
	source_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'	
	genePool = []
	for i in range(0, POOLSIZE):
		gline = []
		for j in range(0, RULESIZE):
			gparts = "".join([random.choice(source_str) for x in xrange(LOCUSSIZE)])
			gline.append(gparts)
		genePool.append(gline)

	return genePool

"""
	ルールが何回データとマッチするかを計算
"""
def score(geneSequence, keyGene):
	scoreValue = 0
	for keyArray in keyGene:
		localScore = 0		
#		for keyUnit in keyArray:
#			if keyUnit in geneSequence: localScore += 1
		for geneCode in geneSequence:
			if geneCode in keyArray: localScore += 1
		if LOCUSSIZE <= localScore: scoreValue += 1
	return scoreValue

"""
	i番目の染色体の適応度を計算
"""
def fitness(geneUnit,keyGene):
	fvalue = 0
	for geneSequence in geneUnit:
		fvalue = fvalue + score(geneSequence, keyGene)
	return fvalue

"""
	遺伝子プールの世代平均適応度の計算
"""
def fave(genePool, keyGene):
	fsum = 0.0
	for geneUnit in genePool:
		fsum = fsum + fitness(geneUnit,keyGene)
	return fsum

"""
	遺伝子プールの出力
"""
def printgene(genePool, keyGene):
	fvalue = 0
	for i, geneUnit in enumerate(genePool):
		printStr = ""
		fvalue = fitness(geneUnit,keyGene)
		if LOWERLIMIT <= fvalue:
			printStr = str(i) + u" : "
			for j, geneSequence in enumerate(geneUnit):
				for wordUnit in geneSequence:
					printStr += wordUnit + u" "
				if j < len(geneUnit) - 1: printStr += u", "
			printStr += u"     " + str(fvalue)
			print printStr
"""
	突然変異
"""
def mutation(genePool):
	source_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	geneSea = []
	for geneUnit in genePool:
		reGeneUnit = []
		for i, geneSequence in enumerate(geneUnit):
			regene = ""
			for j, wordUnit in enumerate(geneSequence):
				if random.random() < MRATE: 
					regene += random.choice(source_str)
				else :
					regene += wordUnit
			print geneSequence + u" -> " + regene
			reGeneUnit.append(regene)		
		geneSea.append(reGeneUnit)

	return geneSea
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


if __name__ == "__main__":
	#キーワードデータの読み込み
	textList = [item.strip() for item in getReadLineList(u"sample1.txt")]
	keyGene = [item.split(u"\t") for item in textList]

	#遺伝子プールの初期化
	genePool = initgene()

	#学習
	for x in xrange(GMAX):
		faveValue = fave(genePool, keyGene)
		print u"第" + str(x) + u"世代 平均適応度 " + str(faveValue)
		printgene(genePool, keyGene)
		genePool = mutation(genePool)
#	print genePool	
 