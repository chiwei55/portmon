#!/usr/bin/python

import os
import time
import sys
import _thread

def _warn(score):
	thershold = 100
	if int(score) > thershold:
		print(score + 'exceeding thershold, warning!!!\n')
	return 0

def _update(score, time, event, info, lock):
	lock.acquire()

	f = open('Report','a')
	newline = time+','+event+','+info+','+score
	f.write(newline+'\n')
	f.close()

	if os.path.isfile('Score'):
	#file exist
		f = open('Score','r')
		total = f.read()
		total = str(int(total) + int(score))
		f.close()
		f = open('Score','w')
		f.write(total)
		f.close()
		_warn(total)
		
	else:
	# first time, open the Score file and initialize it
		f = open('Score','w')
		f.write(score)
		f.close()
		_warn(score)
	
	lock.release()
	return 0

