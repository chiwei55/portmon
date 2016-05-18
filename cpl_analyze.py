#!/usr/bin/python

import time
import sys
import _thread
from update import _update

def _remove_quotes(array):
	return [x[1:-1] for x in array]

def _find_malware(array):
	result = []
	for line in array:
		if line.split(',')[1] == 'process' and line.split(',')[2] == 'created' and 'explorer.exe' in line.split(',')[3]:
			result.append(line.split(',')[4])			
	return result

def _find_behavior(array, categ, act, mainp, subp, lock):
	flag = 0
	if mainp == 'any':
		for line in array:
			if line.split(',')[1] == categ and line.split(',')[2] == act and subp in line.split(',')[4]:
				flag = 1
				#update event and score
				_thread.start_new_thread(_update,('2', str(line.split(',')[0]), str(line.split(',')[1]+' '+line.split(',')[2]), str(line.split(',')[3]+'-->'+line.split(',')[4]), lock))
	else:
		for line in array:
			if line.split(',')[1] == categ and line.split(',')[2] == act and line.split(',')[3] == mainp and subp in line.split(',')[4]:
				flag = 1
				_thread.start_new_thread(_update,('2', str(line.split(',')[0]), str(line.split(',')[1]+' '+line.split(',')[2]), str(line.split(',')[3]+'-->'+line.split(',')[4]), lock))
	return flag

def _cpl_analyze(ctime,ip,lock):
	result = []
	T2 = time.mktime(time.strptime(ctime, '%Y-%m-%d %H:%M:%S'))

	f = open('test_CaputureBatLog','r')
	for line in f.read().splitlines():
		line_array = _remove_quotes(line.split(','))
		T = time.strptime(line_array[0], '%d/%m/%Y %H:%M:%S.%f')
		formaT = time.strftime('%Y-%m-%d %H:%M:%S', T)
		T1 = time.mktime(T)
		categ = line_array[1]
		act = line_array[2]
		mainp = line_array[3]
		subp = line_array[4]
		s ="{0},{1},{2},{3},{4}"
		s = s.format(formaT, categ, act, mainp, subp)
		if abs(T1-T2) <= 60:
			result.append(s)
	f.close()

	hit = 0
	
	#find if cahange the Tracing registry
	hit += _find_behavior(result, 'registry', 'SetValueKey', 'any', 'HKLM\\SOFTWARE\\Microsoft\\Tracing', lock)
	#find if change the ProxySetting
	hit += _find_behavior(result, 'registry', 'SetValueKey', 'any', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Setting', lock)
	hit += _find_behavior(result, 'registry', 'DeleteValueKey', 'any', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Setting', lock)

	suspicious_list = _find_malware(result)
	if len(suspicious_list) != 0:
		for malware in suspicious_list:
			#find if file delete it self
			hit += _find_behavior(result, 'file', 'Delete', 'any', malware, lock)
			#find backup it self and run the backup process
			hit += _find_behavior(result, 'file', 'Write', malware, 'C:\\Users\\ITLAB\\AppData\\Roaming', lock)
			hit += _find_behavior(result, 'process', 'created', malware, 'C:\\Users\\ITLAB\\AppData\\Roaming', lock)
			#find if change the important registry
			hit += _find_behavior(result, 'registry', 'SetValueKey', malware, 'HKCU\\Software\\Microsoft', lock)
		if hit > 0 and ip != 'any':
			pass
			#update black list
	else:
		print ('No suspicious porcess')
		#if ip != 'any', update white list
	return 0
	

