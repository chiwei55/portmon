#!/usr/bin/python

import os
import schedule
import time
import _thread

cmd = "netstat -anop tcp"

def _load():
	f = open('test_log.txt','r')
	content = f.read().splitlines()
	f.close()
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

def _estimate(time):
	os.system('python estimate.py '+time)

def _compare(array):
    if os.path.isfile('test_log_before.txt'):
        #file exists
        last = []

        cur = array[:]
        f = open('test_log_before.txt','r')
        last = f.read().splitlines()

        s1 = set(cur)
        s2 = set(last)
		
#        PortChangeLog = open('PortchangeLog','a')
        if s1.difference(s2):
            for array in s1.difference(s2):
                if array.split(' ')[5] == "LISTENING":
#                    PortChangeLog.write("open  "+time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(time.time()))+" "+array+"\n")
                    print ("Listsning port open, call script for analyze portmon log")
                    print ("CaptureBat execute and analyze")
                    _thread.start_new_thread(_estimate, ("2016-03-22 20:11:12",))	
                    #os.system('python estimate.py 2016-03-22 20:11:12')
                    #os.system('python estimate.py '+time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(time.time())))

        if s2.difference(s1):
            for array in s2.difference(s1):
                pass
#                PortChangeLog.write("Close "+time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime(time.time()))+" "+array+"\n")
#        PortChangeLog.close()
		
        f.close()
    else:
        #file not exists
        pass

def netstat():
	print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
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

#	print (result)
	_compare(result)
		
#	f = open('log','w+')
#	for line in result:		
#		f.write(line)
#		f.write('\n')
#	f.close()

if __name__ =='__main__':
	
	schedule.every(1).minutes.do(netstat)

	while True:
		schedule.run_pending()
#	netstat()
	
