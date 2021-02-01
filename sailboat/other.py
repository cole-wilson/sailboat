# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import re
import sys
from sailboat.plugins import Plugin
import glob
import json
import shutil
import subprocess

licensetext = """# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
class SetVersion(Plugin):
	_type = "build"
	_show = False
	def run(self):
		# try:
		file = open(self.data['short_name'] + os.sep + '__init__.py')
		data = file.read()
		file.close()
		if "__version__" in data:
			data = re.sub("^__version__.*",'__version__ = "{}"  # Added by Sailboat\n'.format(self.version),data,re.MULTILINE)
			data = re.sub("\n__version__.*",'__version__ = "{}"  # Added by Sailboat\n'.format(self.version),data,re.MULTILINE)
		else:
			data = "__version__ = \"{}\"  # Added by Sailboat\n".format(self.version) + data
		file = open(self.data['short_name'] + os.sep + '__init__.py','w+')
		file.write(data)
		file.close()
		# except:
		# 	pass
class BuildDocs(Plugin):
	_type = "build"
	_show = False
	def run(self):
		try:
			os.remove('docs/README.md')
		except:
			pass
		shutil.copy('README.md','docs/index.md')
		o = open('docs/index.md').read()
		a = open('docs/index.md','w+')
		a.write("""---
layout: default
title: Home
nav_order: 1
description: "Sailboat is a Python developer's best friend. It's a Python build tool that can do anything you need it to! It suports a countless number of plugins — you can even [make your own](#plugins). Sailboat is made for anyone, whether you are a beginner on your very first project, or a senior software engineer with years of experience. "
---

<!-- Included twice for docs theme. This file is built, do not edit. Instead edit README.md -->

{}""".format(o).replace('<a style="display:inline-block;" align="center" href="//sailboat.colewilson.xyz">View Documentation Site</a>\n',''))


class Tasks(Plugin):
	description = "Manage 'TODO:' comments"
	_type = "command"
	_show = True
	def run(self):
		prefix = os.path.dirname(os.path.abspath(__file__))+os.sep+'resources'
		if sys.platform.startswith('win'):
			print('windows not yet supported for tasks. if you want, you can help make this possible at github.com/cole-wilson/sailboat')
			return
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
			return
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
					if len(self.options)==2:
						mini = -1*int(self.options[0]) if -1*int(self.options[0]) >1 else -1
						maxi = int(self.options[1]) if int(self.options[1]) >1 else 2
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
					return
				except:
					print('')
			except:
				print('')
				break	