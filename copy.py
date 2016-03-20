#!/usr/bin/python

import os
import schedule
import time

cmd = "netstat -tlnp"

def _load():
	content = []
	content = os.popen(cmd).readlines()
	content.pop(0)
	content.pop(0)
	return content

def _remove_empty(array):
	return [x for x in array if x !='']

def _take_ip_port(array):
	host,port = array.split(':')
	return port

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
    if os.path.isfile('testlog'):
        #file exists
        last = []

        cur = array[:]
        f = open('testlog','r')
        last = f.read().splitlines()

        s1 = set(cur)
        s2 = set(last)
        if s1.difference(s2):
            #print "alert port opened"
            for array in s1.difference(s2):
                rule_cfg = "iptables -I INPUT -p tcp -m tcp --dport {0} -m state --state NEW  -j LOG --log-level 1 --log-prefix \"Track_port{0} \"".format(array.split(' ')[1])
                os.popen(rule_cfg)
                cfg = open('/etc/rsyslog.d/track.conf','a')
                config = ":msg,contains,\"Track_port{0}\" /var/log/tracking/port{0}.log\n".format(array.split(' ')[1])
                cfg.write(config)
                cfg.close()
            os.popen("service rsyslog restart")

        if s2.difference(s1):
            #print "alert port closeed"
            pass

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
		pid,service = _take_pid_service(line_array[6])
		if line_array[0] == "tcp6":
			l_port = _take_ipv6_port(line_array[3])
		else:
			l_port = _take_ip_port(line_array[3])	
		s = "{0} {1} {2} {3}"
		s = s.format(proto, l_port, pid, service)
		result.append(s)

	_compare(result)
		
	f = open('testlog','w+')
	for line in result:
		#print line
		f.write(line)
		f.write('\n')
	f.close()

if __name__ =='__main__':
	
	schedule.every(1).minutes.do(netstat)

	while True:
		schedule.run_pending()
#	netstat()
	
