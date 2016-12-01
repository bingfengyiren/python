#-*- coding:utf-8 -*-
"""
*文本的simhash算法
"""
import os
import sys
import codecs
from mmhash import get_unsigned_hash
import spooky
import farmhash

HASHBITS = 64

class SimHash(object):
	def __init__(self):
		pass

	#[IN]keywords:[(word,weigth),(word,weight)]
	@staticmethod
	def genhash(dataset):
		simhash = [0]*HASHBITS
		for (item,w) in dataset:
			weight = float(w)
			h = SimHash.hashfunc_fm(item)	
			for idx in range(0,HASHBITS):
				if (h >> idx ) & 0x01:
					simhash[idx] += weight
				else:
					simhash[idx] -= weight
		hashCode = 0
		for idx in range(0,HASHBITS):
			if simhash[idx] > 0:
				hashCode |= (0x01 << idx)

		return hashCode

	@staticmethod	
	def hashfunc(item):
		hashv = get_unsigned_hash(item)
		return hashv

	@staticmethod
	def hashfunc_sp(item):
		hashv = spooky.hash64(item)
		return hashv

	@staticmethod
	def hashfunc_fm(item):
		hashv = farmhash.hash64(item)
		return hashv

	@staticmethod
	def ham_dist(hashCode1,hashCode2): 
		ret = (hashCode1 ^ hashCode2)
		dist = 0
		while ret:
			if ret & 1 == 1:
				dist += 1
			ret >>= 1
		return dist

if __name__=="__main__":
	h1=SimHash.genhash([('#九旬母亲病倒 #',233),('孟阿香',216),('智障儿',165),('三次',159)])
	h2=SimHash.genhash([('#九旬母亲病倒 #',233),('孟阿香',216),('智障儿',165),('三载',159)])
	#h1=SimHash.genhash([('#九旬母亲病倒 #',233),('孟阿香',216),('智障儿',165),('三缸',159),('自理能力',157),('稻米',112),('母亲',108),('稻谷',102),('数年',92)],64)
	#h2=SimHash.genhash([('#九旬母亲病倒 #',233),('孟阿香',216),('智障儿',165),('三缸',159),('自理能力',157),('稻米',112),('母亲',108),('稻谷',102),('数载',92)],64)
	print h1
	print h2
	dist = SimHash.ham_dist(h1,h2)
	print dist
