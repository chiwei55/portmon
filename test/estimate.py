#!/usr/bin/python

import time
import sys
import statistics

def _compute(array):
	index = 1
	buf = []
	while index < len(array):
		buf.append(array[index]-array[index-1])
		index = index + 1
	print (buf)
	print (statistics.stdev(buf))

def main():
	result = []

	f = open('test_PortchangeLog','r')
	tag = 0
	array = f.read().splitlines()
	for line in array:
		if line.split(' ')[0] == "open":
			t1 = line.split(' ')[2] +' '+ line.split(' ')[3]
			T1 = time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))
			t2 = sys.argv[1]+' '+sys.argv[2]
			T2 = time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))
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
		tag = tag -1
		print (tag)
		for line in result:	
			if int(line.split(' ')[11]) == tag:
				t = line.split(' ')[2] +' '+ line.split(' ')[3]
				T = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
				buf.append(T)
		if len(buf) > 2:
			_compute(buf)
		print ('\n')
	
if __name__ == '__main__':
	time.sleep(90)
	print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
	main()
