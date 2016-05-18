#!/usr/bin/python

def _remove_quote(array):
	result = []
	for line in array:
		line = line[1:-1]
		result.append(line)
	return result

def main():
	result = []

	f = open('test_CaputureLog','r')

	content = f.read().splitlines()
	for line in content:
		line_array = _remove_quote(line.split(','))
		time = line_array[0]
		reg = line_array[1]
		act = line_array[2]
		caller = line_array[3]
		called = line_array[4]
		s = "{0},{1},{2},{3}"
		s = s.format(reg, act, caller, called)
		result.append(s)

	f.close()

	"""
	new = []	
	for line in result:
		if len(new) == 0:
			new.append(line)
		else:
			exist = 0
			for s in new:
				if line == s:
					exist = 1
			if exist == 0:
				new.append(line)
	"""

	f = open('data_for_arff.txt','w')
	for line in result:
		f.write(line+'\n')
	f.close()

if __name__ == '__main__':
	main()
