#!/usr/bin/python

import os
import schedule
import time

cmd = "netstat -anop tcp"

def _load():
	content = []
	content = os.popen(cmd).read().splitlines()
	content.pop(0)
	content.pop(0)
        content.pop(0)
        content.pop(0)
	return content

def _remove_empty(array):
	return [x for x in array if x !='']

def _take_ip_port(array):
	ip,port = array.split(':')
	return ip,port

def _take_ipv6_port(array):
	s1,s2,s3,port = array.split(':')
	return port

def _take_pid_service(array):
	pid,service = array.split('/')
	if service.find("\n") == -1:
		pass
	else:
		service = service.split('\n')[0]
	return pid,service

def _compare(array):
    if os.path.isfile('log'):
        #file exists
        last = []

        cur = array[:]
        f = open('log','r')
        last = f.read().splitlines()

        s1 = set(cur)
        s2 = set(last)
	PortChangeLog = open('PortchangeLog','a')
        if s1.difference(s2):
	    for array in s1.difference(s2):
		PortChangeLog.write("open  "+time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(time.time()))+" "+array+"\n")

        if s2.difference(s1):
	    for array in s2.difference(s1):
            	PortChangeLog.write("Close "+time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(time.time()))+" "+array+"\n")
            
	PortChangeLog.close()
        f.close()
    else:
        #file not exists
        pass

def netstat():
	content = _load()
	result = []

	for line in content:
		line_array = _remove_empty(line.split(' '))
		proto = line_array[0]
		Host_ip,Host_port = _take_ip_port(line_array[1])
		Ext_ip,Ext_port = _take_ip_port(line_array[2])
		state = line_array[3]
		pid = line_array[4]
		s = "{0} {1} {2} {3} {4} {5} {6}"
		s = s.format(proto, Host_ip, Host_port, Ext_ip, Ext_port, state, pid)
		result.append(s)	
	#print result
	_compare(result)
		
	f = open('log','w+')
	for line in result:		
		f.write(line)
		f.write('\n')
	f.close()

if __name__ =='__main__':
	
	schedule.every(1).minutes.do(netstat)

	while True:
		schedule.run_pending()
#	netstat()
#	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	
