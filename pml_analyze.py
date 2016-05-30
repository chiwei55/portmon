#!/usr/bin/python

import time
import sys
import statistics
import _thread
from update import _update

def _compute(array):
	index = 1
	buf = []
	while index < len(array):
		buf.append(array[index]-array[index-1])
		index = index + 1
	#print (buf)
	#print (statistics.stdev(buf))
	dis = statistics.stdev(buf)
	if dis == 0:
		value = 0
	elif dis <= 45:
		value = 2
	elif dis > 45 and dis < 100:
		value = 1
	else:
		value = 0
	return value

def main(ctime, lock):
	result = []
	f = open('PortchangeLog','r')
	tag = 0
	array = f.read().splitlines()
	for line in array:
		if line.split(' ')[0] == "Close":
			t1 = line.split(' ')[2] +' '+ line.split(' ')[3]
			T1 = time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))
			T2 = time.mktime(time.strptime(ctime, '%Y-%m-%d %H:%M:%S'))
			if (T1-T2) >= 0 and (T1-T2) <= 3600:
				if len(result) == 0:
					line = line+' {}'.format(tag)
					tag = tag + 1
				else:
					for s in result:
						if s.split(' ')[7] == line.split(' ')[7] and s.split(' ')[8] == line.split(' ')[8] and s.split(' ')[9] == line.split(' ')[9] and s.split(' ')[10] == line.split(' ')[10]:
							line = line+' {}'.format(s.split(' ')[11])
							break
					if len(line.split(' ')) == 11:
						line =line+' {}'.format(tag)
						tag = tag + 1
				result.append(line)
	f.close()
	
	while tag > 0:
		buf = []
		event_info = []
		tag = tag -1
		for line in result:	
			if int(line.split(' ')[11]) == tag:
				t = line.split(' ')[2] +' '+ line.split(' ')[3]
				T = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
				buf.append(T)
				event_info.append(line[7:-7])
		if len(buf) > 2:
			value = _compute(buf)
			if value > 0:
				_thread.start_new_thread(_update, (str(value), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "Regular connection", str(event_info), lock))
	return 0

def _pml_analyze(ctime, lock):
	time.sleep(3600)
	main(ctime, lock)
	return 0
