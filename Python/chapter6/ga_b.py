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

GMAX = 10000 #打ち切り世代
MRATE = 0.1 #突然変異率

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

def fitness(geneUnit,keyGene):
	fvalue = 0
	for geneSequence in geneUnit:
		fvalue = fvalue + score(geneSequence, keyGene)
	return fvalue
"""

"""
	i番目の染色体の適応度を計算
"""
def fitness(geneUnit,keyGene):
	fvalue = 0
	fpenalty = 0
	sscore = 0
	totalfitness = 0
	for geneSequence in geneUnit:
		sscore = score(geneSequence, keyGene)
		fvalue = fvalue + sscore
		fpenalty = fpenalty + sscore * sscore

	if len(keyGene) <= fvalue:
		fvalue = len(keyGene)
	totalfitness = fvalue * fvalue - fpenalty
	if totalfitness < 0:
		totalfitness = 0
	return totalfitness



"""
	遺伝子プールの世代平均適応度の計算
"""
def fave(genePool, keyGene):
	fsum = 0.0
	for geneUnit in genePool:
		fsum = fsum + fitness(geneUnit,keyGene)
	f_ave = fsum / POOLSIZE
	return f_ave

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
	ポインタのインクリメント(groulette用）
"""
def gincpoint(point):
	p = point
	p += 1
	if POOLSIZE <= p:
		p = 0
	return p

"""
	ルーレットを回してひとつ遺伝子を選ぶ(交叉用）
"""
def groulette(fvalue, sumf, point):

	#適応度の積算値
	acc=0
	#ルーレットの値を決定
	step = random.randint(1, sumf)

	while acc < step:
		point = gincpoint(point)
		acc += fvalue[point]
	return point

"""
	ポインタのインクリメント
"""
def incpoint(point):
	p = point
	p += 1
	if POOLSIZE * 2 <= p:
		p = 0
	return p

"""
	ルーレットを回してひとつ遺伝子を選ぶ
"""
def roulette(fvalue, sumf):
	acc = 0 						#適応度の積算値
	step = random.randint(1, sumf)	#ルーレットの値を決定
	point = 0

	while acc < step:
		point = incpoint(point);
		acc += fvalue[point] ;

	fvalue[point] = 0 #２度選ばれないようにする
	return point


"""
	一様交叉
"""
def singlecrossover(gp1, gp2, rouletteGene):
	
	geneLine1 = []
	geneLine2 = []
	for (geneSeq1, geneSeq2) in zip(gp1, gp2):
		squenceString1 = ""
		squenceString2 = ""
		for (word1, word2) in zip(geneSeq1, geneSeq2):
			if random.random() < 0.5:
				squenceString1 += word1
				squenceString2 += word2
			else :
				squenceString1 += word2
				squenceString2 += word1
		geneLine1.append(squenceString1)
		geneLine2.append(squenceString2)

	rouletteGene.append(geneLine1)
	rouletteGene.append(geneLine2)

	return rouletteGene

"""
	遺伝子プールの出力
"""
def crossover(genePool, keyGene):
	tempGene = []
	fValue = []
	sumFvalue = 0
	point1 = 0
	point2 = 0

	for geneUnit in genePool:
		fitValue = fitness(geneUnit, keyGene) + 1
		fValue.append(fitValue)
		sumFvalue += fitValue

	for geneUnit in genePool:
		point1 = groulette(fValue,sumFvalue,point2)
		point2 = groulette(fValue,sumFvalue,point1)
		singlecrossover(genePool[point1], genePool[point2], tempGene)	
	return tempGene

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
			reGeneUnit.append(regene)		
		geneSea.append(reGeneUnit)

	return geneSea

"""
	選択
"""
def selection(geneTimesPool, ketGene):

	selectGene = []
	fValue = []
	sumFvalue = 0
	point = 0 		#ルーレットのスタート場所
	midpoint = 0
	
	for geneUnit in geneTimesPool:
		fitValue = fitness(geneUnit, keyGene) + 1
		fValue.append(fitValue)
		sumFvalue += fitValue

	for x in xrange(POOLSIZE):
		midpoint = roulette(fValue, sumFvalue)
		selectGene.append(geneTimesPool[midpoint])

	return selectGene


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
#		printgene(genePool, keyGene)
		tempGene = crossover(genePool, keyGene)
		tempGene = mutation(tempGene)
		genePool = selection(tempGene, keyGene)
	printgene(genePool, keyGene)