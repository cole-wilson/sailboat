from sailboat.plugins import Plugin
import pkg_resources
import os
import glob
import sys
import json
from pathlib import Path
from semver import VersionInfo

import colorama
colorama.init()  # For Windows
import traceback

def refreshEntries():
	plugins={"core":{},"build":{},"release":{},"command":{}}
	for entry_point in pkg_resources.iter_entry_points(group='sailboat_plugins'):
		temp = entry_point.load()
		plugins[temp._type][entry_point.name] = {
			"show" : temp._show,
			"dist" : str(entry_point.dist).split(' ')[0],
			"description" : temp.description,
			"type" : temp._type,
			"release" : temp._release,
			"order" : temp._order,
			"default_os": str(temp._os)
		}
	prefix = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + os.sep
	f = open(prefix +'plugins.json','w+')
	f.write(json.dumps(plugins, indent=2, sort_keys=True))
	f.close()

	del f

class QuickStart(Plugin):
	_type = "core"
	description = "Get your project up and running."

	def runPlugin(self,plug,plugins,opts=[]):
		b = pkg_resources.load_entry_point('sailboat','sailboat_plugins',plug)
		temp = b(
			data=self.data,
			options=opts,
			name=plug,
			prefix=self.prefix,
			version=None
		)
		temp.run(plugins = plugins)
		return temp.data

	def run(self,plugins={},**kwargs):
		input('This quickstart command will get you started on your project.\nFirst, it will set up the config file and your GitHub settings. Then it will add suggested plugins for your project!\n\nPress enter to continue, and ctrl+c to skip a step.')
		for plug in ['wizard', 'git']:
			print("\n\n"+self.red(plug)+"\n"+(len(plug)*"-")+"\n")
			self.data = self.runPlugin(plug,plugins)
		print()
		print("\n\n"+self.red('plugins')+"\n"+(len('plugins')*"-")+"\n")
		pypi = "pypi" if (input('Would you like to generate pypi files for your project? [Y/n]')+"y")[0] == 'y' else ""
		pyinstaller = "pyinstaller" if (input('Would you like to generate pyinstaller files for your project? [Y/n]')+"y")[0] == 'y' else ""
		homebrew = "homebrew" if (input('Would you like to generate homebrew files for your project? [Y/n]')+"y")[0] == 'y' else ""
		combined = f"{pypi} {pyinstaller} {homebrew}"
		if len(combined) > 0:
			print()
			self.runPlugin('add',plugins,opts=[*combined.split()])

		print('Your project is set up, run `sail build` to build, or `sail add <plugin>` to add a new plugin.')

class ManagePlugins(Plugin):
	_type = "core"
	description = "plugin manager."
	def autocomplete(self):
		return ['a','b']
	def run(self,plugins={},**kwargs):
		if self.options == []:
			print("usage: sail plugins [refresh]\n\n\trefresh: reload previously installed plugins.")
		elif self.options == ['refresh'] or self.options == ['-r']:
			refreshEntries();
			print('Done!')
		elif self.options == ['list']:
			print('Build:')
			for x in self.data['build']:
				print('\t- '+x)
			print('Release:')
			for x in self.data['release']:
				print('\t- '+x)
			print('Command:')
			for x in self.data['command']:
				print('\t- '+x)
			
		else:
			print('sailboat: error: invalid option `{}`.'.format(self.options[0]))

class Develop(Plugin):
	_type = "core"
	description = "run your project without building it."
	def run(self,plugins={},**kwargs):
		if os.path.isfile('setup.py'):
			os.system('python setup.py develop')
		else:
			self.info("Can't find setup.py. Create one using sail build.")
class Wizard(Plugin):
	_type = "core"
	description = "configure your project or a plugin."
	setup = { # Top Level Setup
		"name::str":"Full name of your project: ",
		"short_name::str":"Short name of your project: ",
		"email::str":"Email for your project: ",
		"author::str":"Your name(s): ",	
		"short_description::str":"Short description of your project: ",
		"description::str":"Long description of your project: ",
		"url::str":"Home URL of your project",
		"keywords::str":"Your project's keywords, seperated with a a space.",
	}

	def wizard(self):
		super().wizard()
		lt = "BSD-2-Clause/BSD-3-Clause/Apache-2.0/LGPL-2.0/LGPL-2.1/LGPL-3.0/GPL-2.0/GPL-3.0/CCDL-1.0/GNU LGPL/MIT/Other SPDX License ID"
		licen = len(glob.glob('.'+os.sep+'LICENS*'))>0
		if licen:
			if 'license' not in self.data:
				print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
				for license in lt.split(os.sep+''):
					print(f'\t- {license}')
				self.data['license'] = input(">>>\033[0m ")
			else:
				print('\u001b[34mLicense:\u001b[0m {}'.format(self.data['license']))
		else:
			self.data['license'] = "none"
		print(self.section('Resource Settings:'))
		if 'resources' not in self.data:
			self.data['resources']={}
		questions = {
			"icns":"Mac .icns icon for your project, leave blank if none",
			"data_files":"List of all data files for your project seperated with spaces. * counts as wildcard",
			"modules":"Space seperated list of modules required for your project",
			"file":"Main python file of your project. Leave blank if none"
		}
		for key in questions:
			if key in self.data['resources']:
				print(self.blue(questions[key])+': '+str(self.data['resources'][key]))
			else:
				if key in ('modules','data_files'):
					self.data['resources'][key] = input(self.blue(questions[key])+": ").split()
				else:
					self.data['resources'][key] = input(self.blue(questions[key])+": ")
		self.data['name'] = self.data['name'].replace(' ','_')
		self.data['short_name'] = self.data['short_name'].replace(' ','_')
		
		print(self.red('Be sure to prefix any paths to any resources with \u001b[4m`os.path.dirname(os.path.abspath(__file__))+os.sep`\u001b[0m\033[1;31m to make sure that they use the correct path and not the current directory.'))
	def run(self,plugins={}):
		if self.options == []:
			self.wizard()
			for tt in ['command','build','release']:
				for x in self.data[tt]:
					print(self.section(x.title()+":"))
					dist = plugins[tt][x]['dist']
					b = pkg_resources.load_entry_point(dist,'sailboat_plugins',x)
					b = b(
							data=self.data,
							options=[],
						name=x,
						prefix=self.prefix,
							version=None
					)
					try:
						b.wizard()
					except KeyboardInterrupt:
						print('Abborted by user')
					except BaseException:
						print(traceback.print_exception(*sys.exc_info()))
						print('Error in `{}` wizard script:\n\t{}'.format(x,traceback.print_exception(*sys.exc_info())))
					self.data[tt][x] = b.data[tt][x]
			
		else:
			for x in self.options:
				if x in plugins['command']:
					t = 'command'
				elif x in plugins['release']:
					t = 'release'
				elif x in plugins['build']:
					t = 'build'
				else:
					print("Couldn't find the {} plugin.".format(x))
					continue
				dist = plugins[t][x]['dist']
				temp = pkg_resources.load_entry_point(dist,'sailboat_plugins',x)
				temp = temp(
					data=self.data,
					options=[],
					name=x,
					prefix=self.prefix,
					version=None
				)
				try:
					temp.wizard()
				except KeyboardInterrupt:
					print('Abborted by user')
				except BaseException as e:
					print('Error in `{}` wizard script:\n\t{}'.format(x,e))
				self.data[t][x] = temp.data[t][x]

class Git(Plugin):
	_type = "core"
	description = "Manage Git for your project."

	def run(self,plugins={},**kwargs):
		if self.options == ['push']:
			a = input("Message: ").replace('"',r'"')
			os.system(f'git add .;git commit -a -m "{a}";git push;')
			return
		if 'github' not in self.data['git']:
			uname = input('GitHub username: ')
			if input('Do you have a GitHub repository for this project yet?')[0]=='y':
				self.data['git']['github'] = uname+'/'+input('GitHub repo name: ')
			else:
				print('Go to https://github.com/new and create a repo.')
				self.data['git']['github'] = uname+'/'+input('GitHub repo name: ')
			os.system(f"""git init;
git add .;
git config --global credential.helper "cache --timeout=3600";
git config user.name "{self.data["author"]}";
git config user.email "{self.data["email"]}";
git commit -m "Initial Commit :rocket:";
git remote add origin https://github.com/{self.data['git']['github']}.git;
git push -u origin master;
""")
		print('Your GitHub repo is setup. To update your repo, type:\n\n\tgit add .;git commit -a -m "Your message here";git push;\n\nin your terminal, or `sail git push`')

class GithubRelease(Plugin):
	_type = "release"
	description = "GitHub Tagged Release"
	def release(self):
		os.system(f"""git init;
git add .;
git config --global credential.helper "cache --timeout=3600";
git config user.name "{self.data["author"]}";
git config user.email "{self.data["email"]}";
git commit -m "{self.data['release-notes']}";
git tag v{self.version};
git remote add origin https://github.com/{self.data['git']['github']}.git||echo origin already added;
git push -u origin master --tags;
""")

class Release(Plugin):
	_type = "core"
	description = "Release your project."
	def run(self,plugins={},**kwargs):
		self.data['release-notes'] = input('Release Notes: ')
		version = VersionInfo.parse(self.data['latest_build'])
		version = str(VersionInfo(major=version.major,minor=version.minor,patch=version.patch,prerelease=version.prerelease))
		runs = {}
		if self.options == []:
			for x in self.data['release']:
				if x in plugins['release']:
					runs[x] = plugins['release'][x]['order']
			for x in self.data['build']:
				if x in plugins['build']:
					if plugins['build'][x]['release']:
						runs[x] = plugins['build'][x]['order']
			for x in self.data:
				if x in plugins['core']:
					if plugins['core'][x]['release']:
						runs[x] = plugins['core'][x]['order']
			
		else:
			for x in self.options:
				if x in self.data['release'] and x in plugins['release']:
					runs[x] = plugins['release'][x]['order']
				elif x in self.data['build']:
					if plugins['build'][x]['release']:
						runs[x] = plugins['build'][x]['order']
				elif x in self.data:
					if plugins['core'][x]['release']:
						runs[x] = plugins['core'][x]['order']
				
				else:
					print('sailboat: error: {} is not a valid release plugin.'.format(x))
					return
		runstemp = []
		for x in runs:
			runstemp.append(f"{runs[x]}::{x}")
		runstemp.sort()
		runs = []
		for x in runstemp:
			order,name = x.split('::')
			runs.append(name)
		input(f'Press enter to release version {version} the following ways:\n\t- '+'\n\t- '.join(runs)+'\n\n>>>')
		dones = []
		lorder = 0
		for release_plugin in runs:
			if release_plugin in dones:
				continue
			print(self.section(release_plugin+":"))
			if release_plugin in self.data['release']:
				dist = plugins['release'][release_plugin]['dist']
			elif release_plugin in self.data['build']:
				dist = plugins['build'][release_plugin]['dist']
			else:
				dist = plugins['core'][release_plugin]['dist']
			temp = pkg_resources.load_entry_point(dist,'sailboat_plugins',release_plugin)
			temp = temp(
				data=self.data,
				options=[self.options],
				name=release_plugin,
				prefix = self.prefix,
				version=version
			)
			temp.release()
			if temp._type == 'core':
				self.dat = temp.data
			else:
				self.data[temp._type][release_plugin] = temp.data[temp._type][release_plugin]
			dones.append(release_plugin)
			lorder = order
		print()
		self.data['latest_release'] = version

		


class Remove(Plugin):
	_type = "core"
	description = "remove a plugin from you project."
	def run(self,plugins,**kwargs):
		if len(self.options)<1:
			print('usage: sail remove [plugin ...]\n\n\tRemoves plugins from project.')
			return
		for option in self.options:
			t = ''
			if option in plugins['command'].keys():
				t = 'command'
			if option in plugins['release'].keys():
				t = 'release'
			if option in plugins['build'].keys():
				t = 'build'
			if t=='':
				print('couldn`t find {}, therfore not removed.'.format(option))
			else:
				try:
					del self.data[t][option]
					print('removed {}'.format(option))
				except KeyError:
					print('couldn`t find {}, therfore not removed.'.format(option))

class Add(Plugin):
	_type = "core"
	description = "add a plugin to your project."
	def run(self,**kwargs):
		# get all availbile plugin
		done = []
		if len(self.options)==0:
			print('''usage: sail add [plugins ...]

	Install PLUGINS to current project.
	''')
		for point in pkg_resources.iter_entry_points('sailboat_plugins'):
			if (point.name in self.data['build'] or point.name in self.data['command'] or point.name in self.data['release']) and point.name in self.options:
				print('{} already added'.format(point.name))
				continue
			if point.name in self.options:
				done.append(point.name)
				temp = point.load()
				run = temp(data=self.data,options=[],name=point.name,prefix=self.prefix)
				print(self.section(f'{point.name} [{run._type}]:{run.description}.'))
				if point.name not in self.data[run._type]:
					self.data[run._type][point.name] = {}
				if run._type == 'core':
					print('BE WARNED: THIS PLUGIN TYPE IS REGISTERED AS "core", which means it has unfiltered access to your project`s data. Please be 100% sure you want to do this.')
				run.data = self.data
				try:
					run.wizard()
					run.add()
				except KeyboardInterrupt:
					print('Aborted by user')
				except BaseException as e:
					print('Error in `{}` wizard script:\n\t{}'.format(point.name,e))
				data = run.data
				self.data[run._type][point.name] = data[run._type][point.name]
				print('added {}'.format(point.name))
		for x in self.options:
			if x not in done and (x not in self.data['build'] and x not in self.data['command'] and x not in self.data['release']):
				print('error: could not find {}, please make sure you have downloaded it.'.format(x))
		refreshEntries()
		return self.data

class Actions(Plugin):
	description = "Generate a GH Actions workflow file."
	_type = "core"
	
	def run(self,plugins,**kwargs):
		linux = ""
		mac = ""
		windows = ""
		for x in self.data['build']:
			if 'windows' in plugins['build'][x]['default_os']:
				windows = windows + " " + x
			if 'linux' in plugins['build'][x]['default_os']:
				linux = linux + " " + x
			if 'mac' in plugins['build'][x]['default_os']:
				mac = mac + " " + x

		with self.getResource(f'resources{os.sep}sailboat.yml.template') as temp:
			new = temp.read().format(
				linux=linux,
				mac=mac,
				windows=windows,
				l="#" if linux == "" else "",
				m="#" if mac == "" else "",
				w="#" if windows == "" else "",
				**self.data,
				dependencies = " ".join(self.data['resources']['modules'])
			)
			try:
				f = open(f'.github{os.sep}workflows{os.sep}sailboat.yml','w+')
			except:
				os.mkdir('.github')
				os.mkdir(f'.github{os.sep}workflows')
				f = open(f'.github{os.sep}workflows{os.sep}sailboat.yml','w+')
			f.write(new)
			f.close()
		
		print('Workflow generated. Remember to push twice in order for new workflow to take effect.')