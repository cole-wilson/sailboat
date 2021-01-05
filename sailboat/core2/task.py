# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import re
import sys

prefix = os.path.dirname(os.path.abspath(__file__))+os.sep+'resources'

def main(ids):
	if sys.platform.startswith('win'):
		print('windows not yet supported for tasks. if you want, you can help make this possible at github.com/cole-wilson/sailboat')
		sys.exit(0)
	tasks = []
	for root,dirs,files in os.walk('.'):
		for filename in files:
			x = os.sep.join((root,filename))
			if x.endswith('.py'):
				f = open(x)
				content = f.read()
				f.close()
				for a in re.findall(r'^.*(#\s*?[tT][oO][dD][oO]:\s?)(.*?)$',content,re.M):
					tasks.append((a,x))
	if len(tasks)==0:
		print('NO TASKS!')
		sys.exit(0)
	while True:
		os.system('clear')
		print('\u001b[36m\u001b[4mTODOS:\u001b[0m'.rjust(6))
		print()
		for count,task in enumerate(tasks):
			print(f"{(str(count+1)+'.').ljust(4)}\t{task[0][1].ljust(20)}\t\t({task[1].ljust(10)})")
		try:
			ch = input('\n\nEnter a task number to view code.\n>>> ')
			try:
				ch = int(ch)-1
				content = open(tasks[ch][1]).read()
				content = content.split('\n')
				for count,line in enumerate(content):
					if tasks[ch][0][0] in line:
						linenum = count+1
						break
				line = line.replace(tasks[ch][0][0]+tasks[ch][0][1],'')#.replace('\t','')
				if len(sys.argv)==4:
					mini = -1*int(sys.argv[2]) if -1*int(sys.argv[2]) >1 else -1
					maxi = int(sys.argv[3]) if int(sys.argv[3]) >1 else 2
				else:
					mini,maxi = -6,6
				tabsmax = []
				for x in range(mini,maxi):
					tabsmax.append(content[count-x].count('\t'))
				tab = "\t"
				print(f"\n\n\n{linenum+mini}\u001b[32m ... \u001b[31m{content[count+mini].replace(tab,'',min(tabsmax))}\u001b[0m")
				for x in range(mini+1,0):
					print(f"{linenum+x}\u001b[32m ... \u001b[31m{content[count+x].replace(tab,'',min(tabsmax))}\u001b[0m")
				print(f"\u001b[33m{linenum}\u001b[32m ... \u001b[31m{line.replace(tab,'',min(tabsmax))}\u001b[34m\u001b[4m{tasks[ch][0][0]}{tasks[ch][0][1]}\u001b[0m")
				for x in range(1,maxi-1):
					print(f"{linenum+x}\u001b[32m ... \u001b[31m{content[count+x].replace(tab,'',min(tabsmax))}\u001b[0m")
				input(f"{linenum+maxi-1}\u001b[32m ... \u001b[31m{content[count+maxi-1].replace(tab,'',min(tabsmax))}\u001b[0m\n\n\n(press enter)")
			except KeyboardInterrupt:
				print()
				sys.exit(0)
			except KeyboardInterrupt:
				print('')
		except KeyboardInterrupt:
			print('')
			break	