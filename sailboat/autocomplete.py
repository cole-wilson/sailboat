import os
import sys

prefix = os.path.dirname(os.path.abspath(__file__))+os.sep

try:
	f = open(prefix+'autocomplete','r')
	data = f.read().split('\n')
	f.close()
except:
	sys.exit()

for line in data.__reversed__():
	if line == "" or line.startswith('#'):
		continue
	stub = line.split('::')[0]
	completes = line.split('::')[1]
	already_typed = " ".join(sys.argv[1].split(' ')[:-1])
	if stub == already_typed:
		print(completes)
