# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import glob
import toml
import sys
import shutil


def main():
	"""
	The setup wizard for sailboat
	"""
	prefix = os.path.dirname(os.path.abspath(__file__))+os.sep+'resources'
	data = {}
	if os.path.isfile('.'+os.sep+'sailboat.toml'):
		try:
			data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
		except toml.decoder.TomlDecodeError as e:
			print('Config error:\n\t'+str(e))
			exit()
	print("I'm going to ask you a few questions about your project to create a config file!\n\nPlease fill in everything to your ability. If you can't provide a value, leave it blank.\n")
	# GENERAL ================================================
	def red(string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\033[1;31m"+str(string)+"\033[0m"
	def blue(string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\033[1;34m"+str(string)+"\033[0m"
	def section(string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\n\u001b[4m\u001b[1;36m"+str(string)+"\u001b[0m"

	# GENERAL ================================================
	print(section('General Configuration:'))
	questions = {
		"name":"Full name of project",
		"short_name":"Short name of project (unique)",
		"author":"Your name(s)",
		"email":"Project email",
		"short_description":"Short description of your project",
		"description":"Full description of your project",
		"url":"Main project URL",
		"keywords":"Keywords seperated with a space",
		'license':"You seem to have a license file in your project, but what type is it?\n\t- "+(f"\n\t- ".join(lt.split('/'))+"\n>>>")
	}

	licen = len(glob.glob('.'+os.sep+'LICENS*'))>0

	lt = "BSD-2-Clause/BSD-3-Clause/Apache-2.0/LGPL-2.0/LGPL-2.1/LGPL-3.0/GPL-2.0/GPL-3.0/CCDL-1.0/GNU LGPL/MIT/Other SPDX License ID"
	licen = len(glob.glob('.'+os.sep+'LICENS*'))>0
	if licen:
		if 'license' not in self.data:
			print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
			for license in lt.split(os.sep+''):
				print(f'\t- {license}')
			self.data['license'] = input(">>>\033[0m ")
		else:
			print('License: {}'.format(self.data['license']))


	for key in questions:
		if key not in data:
			if key=='license':
				if licen:
					print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
					for license in lt.split(os.sep+''):
						print(f'\t- {license}')
					data[key] = input(">>>\033[0m ")
				else:
					data[key] = 'None'
			else:
				data[key] = input(blue(questions[key])+": ")
		else:
			print(blue(questions[key])+": "+str(data[key]))

	# resource
	print(section('Resource Settings:'))
	if 'resources' not in data:
		data['resources']={}
	questions = {
		"icon":"Square .png icon for your project, leave blank if none",
		"data_files":"List of all data files for your project seperated with spaces. * counts as wildcard",
		"modules":"Space seperated list of modules required for your project",
		"file":"Main python file of your project. Leave blank if none"
	}
	for key in questions:
		if key in data['resources']:
			print(blue(questions[key])+': '+str(data['resources'][key]))
		else:
			if key in ('modules','data_files'):
				data['resources'][key] = input(blue(questions[key])+": ").split()
			else:
				data['resources'][key] = input(blue(questions[key])+": ")
	print(red('Be sure to prefix any paths to any resources with \u001b[4m`os.path.dirname(os.path.abspath(__file__))+os.sep`\u001b[0m\033[1;31m to make sure that they use the correct path and not the current directory.'))

# build
	print(section('Build Settings:'))
	if 'build' not in data:
		data['build']={}
	questions = {
		"type":"Please choose one of the following options for your project:\n\t1. My project only deals with text (not graphical).\n\t2. My project is a graphical app.\n>>>",
		"homebrew":"Would you like to distribute a Homebrew app for your project? [y/n]",
		"unix":"Would you like to distribute a Unix executable for your project? [y/n]",
		"mac":"Would you like to distribute a Mac app for your project? [y/n]",
		"windows":"Would you like to distribute a Windows app for your project? [y/n]",
		
	}
	for key in questions:
		if key in data['build']:
			print(blue(questions[key])+': '+str(data['build'][key]))
		else:
			if "[y/n]" in questions[key]:
				data['build'][key] = input(blue(questions[key])+": ")[0]=='y'
			else:
				data['build'][key] = input(blue(questions[key])+": ")
	if data['build']['type']=="1":
		print(red('Be sure to add some user input in your script, or else the window will close too quickly!'))
	if (data['build']['mac'] or data['build']['windows']):
		if 'installer' in data['build']:
			print(blue("Would you like to provide an installer for the Windows app? (recomended) [y/n]: ")+str(data['build']['installer']))
		else:
			data['build']['installer'] = input(blue("Would you like to provide an installer for the Windows app? (recomended) [y/n]: "))[0]=="y"
	if (not data['build']['mac'] and not data['build']['windows']):
		data['build']['installer'] = False
	if not sys.platform.startswith('win') and data['build']['windows']:
		print(red('You can only make a Windows app on a Windows computer.'))
		needswin=True
	else:
		needswin=False
	if sys.platform != 'darwin' and data['build']['mac']:
		print(red('You can only make a Mac app on a Mac.'))
		needsmac=True
	else:
		needsmac=False

	try:
		asd=data['build']['actions']
	except:
		asd=False

	if (needsmac or needswin) or asd:
		if ('actions' in data['build']):
			print(blue('Github Actions can build your app on the cloud for free.\n\033[1;31mWould you like to use that to build your apps? [y/n]: ')+str(data['build']['actions']))
			actions = data['build']['actions']
		else:
			actions=input('\033[1;34mGithub Actions can build your app on the cloud for free.\n\033[1;31mWould you like to use that to build your apps? [y/n]: \033[0m')[0]=='y'
			data['build']['actions'] = actions
	else:
		actions = False
		data['build']['actions'] = False
	if 'commands' in data['build']:
		print(blue('Commands: ')+str(data['build']['commands']))
	else:
		print(section('Terminal Commands:'))
		if input(blue('Does your project have any terminal commands associated with it? [y/n]: '))[0]=='y':
			data['build']['commands'] = {}
			print(red('`runs:` must be follow the rule \u001b[4m`module.function_name`\u001b[0m\033[1;31m, or be blank, which runs the main project file as a script. \n\nIt is recommended to use function wrappers.\n\nAn example would be:\n\t- name: test_command\n\t  runs: file.test\nThis would run the test() function in file.py\n\nPress ctrl+c to stop asking.'))
			while True:
				try:
					n = input(blue('\t- name: '))
					mod = input(blue('\t  runs: '))
					data['build']['commands'][n]=mod
					print()
				except KeyboardInterrupt:
					print('\nDone!\n\n')
					break
		else:
			data['build']['commands'] = {}

	installl = ''
	if data['build']['mac'] or data['build']['mac'] or data['build']['actions']:
		installl = "### " + " and ".join(["Mac" if data['build']['mac'] else "","Windows" if data['build']['mac'] else "","Unix" if data['build']['actions'] else ""])+f"\nGet the executable from the [latest release](/releases/latest)."
		runn = " or run the application file."
	else:
		runn = "."


	if os.path.isfile('README.md'):
		print(section('README:'))
		if input('\033[1;34mOverwrite current README.md? [y/n]:\033[0m ')[0]=='y':
			open('README.md','w+').write(open(prefix+os.sep+'readme.template.md').read().format(**data,other_install=installl,other_run=runn))
	else:
		open('README.md','w+').write(open(prefix+os.sep+'readme.template.md').read().format(**data,other_install=installl,other_run=runn))

	# Other
	if 'bundle_id' not in data['build']:
		data['build']['bundle_id'] = f"com.{data['author'].lower().replace(' ','')}.{data['short_name']}"
	if 'homebrew' not in data['build']:
		data['build']['homebrew'] = False
	data['name']=data['name'].replace(' ','_').replace('/','-')

	print(section('Git Settings:'))
	if 'git' not in data:
		data['git'] = {}
	print(blue('Please run `sailboat git` to setup GitHub.'))


	f = open('.'+os.sep+'sailboat.toml','w+')
	f.write(toml.dumps(data))
	f.close()

	print('\n\n\033'+red(section('`sailboat.toml` has been created. Please edit that for further changes and advanced options.\033[0m')))