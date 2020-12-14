# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import sys
import toml
import glob
import shutil
import re
import requests

prefix = os.path.dirname(os.path.abspath(__file__))+os.sep+'resources'


def main(version,arguments,nointeraction=False):
	# ============== Get Data ===============================================
	if not os.path.isfile('.'+os.sep+'sailboat.toml'):
		print('Please create a config file with `sailboat wizard` first.')
		sys.exit(0)
	try:
		data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
	except toml.decoder.TomlDecodeError as e:
		print('Config error:\n\t'+str(e))
		exit()
	# ============== Pre-build script ===============================================
	if 'build_script' in data['build']:
		try:
			buildscript = __import__(data['build']['build_script'].replace('.py',''))
		except BaseException as e:
			print('Error with custom prebuild script:\n'+str(e))
			pass
	try:
		newdata = buildscript.pre(version,data)
		if isinstance(newdata,dict):
			data = newdata
	except BaseException as e:
		print('Error with custom prebuild script:\n\t`'+str(e)+"`")
		pass
	# ============== Show what will happen ===============================================
	print('This command will build the following:')
	print('\t- Generate a correct directory structure, setup.py, .gitignore, etc...')
	only=False
	for x in arguments:
		if '-only' in x[0]:
			only=True
			break
	dopypi,dobrew,domac,dowin,doact,doset=False,False,False,False,False,False
	if only:
		if ('--pypi-only','') in arguments:
			dopypi = True
		elif ('--homebrew-only','') in arguments:
			dobrew = True
		elif ('--windows-only','') in arguments and sys.platform.startswith('win'):
			dowin = True
		elif ('--mac-only','') in arguments and sys.platform.startswith('darwin'):
			domac = True
		elif ('--actions-only','') in arguments:
			doact = True
		elif ('--setup-only','') in arguments:
			doset = True
		
	else:
		dopypi = True
		dobrew = data['build']['homebrew']
		dowin = data['build']['windows'] and sys.platform.startswith('win')
		domac = data['build']['mac'] and sys.platform.startswith('darwin')
		doact= data['build']['actions']
		doset=True
	if ('--no-installer','') in arguments:
		doinstall=False
	else:
		doinstall=data['build']['installer']
	if dopypi:
		print('\t- A distributable Python module.')
	if dobrew:
		print('\t- A Homebrew formula.')
	if dowin:
		installer = " with a .msi installer." if doinstall else "."
		print('\t- A Windows app'+installer)
	if domac:
		installer = " with a .dmg installer." if doinstall else "."
		print('\t- A Mac app'+installer)
	if doact:
		print('\t- A GitHub Actions file for building Mac and Windows apps and publishing a Github release.')
	if not nointeraction:
		input('Press enter to continue.')
	# ============== Create bin Script ===============================================
	try:
		os.mkdir('bin')
	except:
		pass
	bins = []
	for commandname in data['build']['commands'].keys():
		if data['build']['commands'][commandname] == '':
			open("bin"+os.sep+commandname,'w+').write(f"#!"+os.sep+"usr"+os.sep+"bin"+os.sep+f"env bash\npython3 -m {data['short_name']} $@")
			bins.append('bin'+os.sep+commandname)
	# ============== Get module names ===============================================

	if 'no_import' not in data['resources']:
		data['resources']['no_import'] = []
	mods = []
	for x in glob.glob(data['short_name']+os.sep+'*.py'):
		f = open(x)
		mods += re.findall('(?m)(?:from[ ]+(\S+)[ ]+)?import[ ]+(\S+)(?:[ ]+as[ ]+\S+)?[ ]*$',f.read())
		f.close()
	modules = []
	for x in mods:
		modules.append(x[1].split('.')[0])
	for module in set(modules):
		if module not in data['resources']['no_import'] and ( module!= data['short_name'] and module not in sys.builtin_module_names and module not in data['resources']['modules']):
			print('Checking for {} on PyPi...'.format(module))
			response = requests.get("https://pypi.python.org/pypi/{}/json".format(module))
			if response.status_code == 200:
				data['resources']['modules'].append(module)
			else:
				data['resources']['no_import'].append(module)

	# ============== Generate setup.py ===============================================
	if doset:
		if 'custom_setup' in data:
			cu=str(data['custom_setup'])
		else:
			cu=str({})
		with open(prefix+os.sep+'setup.py.template') as datafile:
			template = datafile.read()

		entries = []
		for commandname in data['build']['commands'].keys():
			if data['build']['commands'][commandname]!="":
				modname = ".".join(data['build']['commands'][commandname].split('.')[:-1])
				funcname = data['build']['commands'][commandname].split('.')[-1]
				entries.append(commandname+"="+data["short_name"]+"."+modname+":"+funcname)

		setup = template.format(
			**data,
			**data['resources'],
			cu=cu,
			bins=bins,
			version = version,
			entry_points = entries
			
		)
		open('setup.py','w+').write(setup)

	# ============== Generate directory structure ===============================================
	if not os.path.isfile('.gitignore'):
		open('.'+os.sep+'.gitignore','w+').write(open(prefix+os.sep+'gitignore.template').read().replace('/',os.sep))
	source_dir = os.getcwd()
	target_dir = data["short_name"]+os.sep
	types = ('*.py',*data['resources']["data_files"])
	file_names = []
	for files in types:
		file_names.extend(glob.glob(files))
	if not os.path.isdir(target_dir):
		os.mkdir(target_dir)
	try:
		bs = data['build']['build_script']
	except:
		bs = "RANDOM-----edfskjsdhflkjdhflksdjhflkasjdhflkasjdhflkasjdhflkajsdhflkjadshf"
	for file_name in file_names:
		if file_name in ("setup.py","sailboat.toml",bs):
			continue
		shutil.move(os.path.join(source_dir, file_name), target_dir+os.sep+file_name)
	for filename in glob.glob(target_dir+os.sep+'LICE*'):
		shutil.copyfile(filename,'LICENSE')
	if not os.path.isfile(target_dir+'__init__.py'):
		open(target_dir+'__init__.py','w+').write('# This file must exist, empty or not')
	if data['resources']['file']!="" and not os.path.isfile(data['short_name']+os.sep+'__main__.py'):
		try:
			os.rename(data['short_name']+os.sep+data['resources']['file'],data['short_name']+os.sep+'__main__.py')
			open(data['short_name']+os.sep+data['resources']['file'],'w+').write('# Please edit __main__.py for the main code. Thanks!\n(you can delete this file.)')
		except FileNotFoundError:
			pass
	# ============== Generate pypi files ===============================================
	if dopypi:
		try:
			shutil.rmtree('dist')
		except:
			pass
		os.system('python3 .'+os.sep+'setup.py bdist_wheel sdist -d dist'+os.sep+'pypi')
		try:
			shutil.rmtree('build')
		except:
			pass
		for x in glob.glob('dist'+os.sep+'*.whl'):
			os.rename(x,x.replace('dist'+os.sep,'dist'+os.sep+'pypi'+os.sep))
		for x in glob.glob('*.egg-info'):
			shutil.rmtree(x)

	# ============== Generate homebrew file ===============================================
	if dobrew:
		retmp = '\tresource "{name}" do\n\t\turl "{url}"\n\t\tsha256 "{sha256}"\n\tend\n'
		resources = ''
		for modulename in data['resources']['modules']:
			req = requests.get('https://pypi.org/pypi/{}/json'.format(modulename)).json()
			versionPy = req['info']['version']
			url = req['releases'][versionPy][0]['url']
			sha256 = req['releases'][versionPy][0]['digests']['sha256']
			if not (url.endswith('.tar.gz') or url.endswith('.zip')):
				try:
					url = req['releases'][versionPy][1]['url']
					sha256 = req['releases'][versionPy][1]['digests']['sha256']
				except:
					continue
			resources+=retmp.format(name=modulename,url=url,sha256=sha256)
		os.mkdir('dist'+os.sep+'homebrew')
		f = open('dist'+os.sep+'homebrew'+os.sep+'{name}.rb'.format(name=data['name']),'w+')
		f.write(open(prefix+os.sep+'brew.rb').read().format(
			**data,
			resources2 = resources
		))
		f.close()
	# ============== Generate w/Pyinstaller ===============================================
	if dowin or domac:
		try:
			import PyInstaller.__main__
		except:
			print('Installing PyInstaller...')
			os.system('pip3 install pyinstaller')
			import PyInstaller.__main__
		
		mods = []
		for x in data['resources']['modules']:
			mods.append('--hidden-import')
			mods.append(x)

		datafiles = []
		for x in data['resources']['data_files']:
			for g in glob.glob(data['short_name']+os.sep+x):
				datafiles.append('--add-data')
				datafiles.append(g+os.pathsep+g.replace(data['short_name']+os.sep,''))
		typ = '--nowindowed' if data['build']['type']=='1' else '--noconsole'

		ico = ['--icon',data['resources']['icon']] if 'icon' in data['resources'] else []
		options = [
			data['short_name']+os.sep+'__main__.py',
			'--onefile',
			'--name',
			data['name'] if ('-n','')not in arguments else 'app',
			'--distpath',
			'.'+os.sep+'dist'+os.sep+'pyinstaller',
			*mods,
			*datafiles,
			typ,
			*ico,
			'--osx-bundle-identifier',
			data['build']['bundle_id']
		]
		print(options)
		PyInstaller.__main__.run(options)
		try:
			print('removing '+data['name']+".spec...")
			os.remove(data['name']+".spec")
		except:
			print('removing app.spec...')
			os.remove("app.spec")			
	# ============== Generate Installer Package ===============================================

	if not doinstall and False:
		pass
	elif sys.platform.startswith('win') and False:#WINDOWS
		os.system('pip install distro')
		os.system('pip install git+https://github.com/x24git/wixpy')
		d = open(prefix+os.sep+'wixpy.template.json').read().format(
			**data,
			version=version,
			icns=data['icon'],
			keywo=", ".join(data['keywords'])
		)
		open('wixpy.json','w+').write(d)
		print(d)
		print('STARTING WIXPY...')
		os.system('wix.py wixpy.json')

	elif sys.platform.startswith('darwin'):#MAC
		try:
			import dmgbuild
		except:
			print('Installing dmgbuild')
			os.system('pip3 install dmgbuild')
			import dmgbuild
		del dmgbuild
		open('build'+os.sep+'settings.py','w+').write(open(prefix+os.sep+'settings.py.template').read().format(
			**data,
			version=version,
			icns=data['icon'],
			keywo=", ".join(data['keywords'])
		))
		os.system(f'cat build/settings.py;dmgbuild -s .{os.sep}build{os.sep}settings.py "{data["name"]}" ./dist/pyinstaller/{data["name"]}.dmg')

	else:
		print(f'Installer creation not yet supported for {sys.platform}!')
	# ============== Generate Github Actions Workflow ===============================================
	if doact:
		try:
			oldact = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml').read().split('\n')[0]
		except:
			oldact="\n"
		try:
			f = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml','w+')
		except:
			os.system('mkdir -p .github'+os.sep+'workflows'+os.sep)
			f = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml','w+')
		newdata = open(prefix+os.sep+'sailboat.yml.template').read().format(
			**data,
			mac=""if data['build']['mac']else"#",
			windows=""if data['build']['windows']else"#",
			win_ext=".exe"if data['build']['installer']else".exe",
			mac_ext=".dmg"if data['build']['installer']else"",
		).replace('\t','  ')
		f.write(newdata)

		f.close()
		newact = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml').read().split('\n')[0]
		data['build']['actions_built_latest'] = newact != oldact
		print(oldact)
		print(newact)
	# ============== Post build ===============================================
	try:
		newdata = buildscript.post(version,data)
		if isinstance(newdata,dict):
			data = newdata
	except:
		pass
	# ============== Save Version ===============================================
	data['latest_build'] = version
	open('sailboat.toml','w+').write(toml.dumps(data))
	os.system('python .'+os.sep+'setup.py develop')