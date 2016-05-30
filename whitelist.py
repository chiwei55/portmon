#!/usr/bin/python
import os

def _whitelist(ip, lock):
	lock.acquire()

	exist = 0
	result = []

	f = open('whitelist','r')

	if os.stat('whitelist').st_size != 0:
		for line in f.read().splitlines():
			if ip == line.split(',')[0]:
				exist = 1
				hit = int(line.split(',')[1])+1
				newline = line.split(',')[0]+','+str(hit)
				result.append(newline)
			else:
				result.append(line)
	
	if exist == 0:
		# ip do not exist in cache
		if len(result) > 100:
			#cache is full,compute threshold T
			hit_total = 0
			for line in result:
				hit_total += int(line.split(',')[1])
			T = round(hit_total/len(result))

			result = result[::-1]
			for line in result:
				if int(line.split(',')[1]) > T:
					index = result.index(line)
					newline = line.split(',')[0]+','+str(T)
					result.remove(line)
					result.insert(index, newline)
				else:
					newline = ip+',1'
					result.remove(line)
					result.insert(len(result), newline)
					break
			result = result[::-1]		
				
		else:
			#cache is not full, append new ip
			newline = ip+',1'
			result.append(newline)

	f.close()

	f = open('whitelist','w')	
	for line in result:
		f.write(line)
		f.write('\n')
	f.close()

	lock.release()

	return 0
