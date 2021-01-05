# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import sys
import toml
import shutil
import requests
import time

def main(arguments,ids):
	if not os.path.isfile('.'+os.sep+'sailboat.toml'):
		print('Please create a config file with `sailboat wizard` first.')
		sys.exit(0)
	try:
		data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
	except toml.decoder.TomlDecodeError as e:
		print('Config error:\n\t'+str(e))
		exit()
	if ('-f','') not in arguments:
		try:
			latestag = os.popen('git tag').read().split('\n')[-2]
		except:
			latestag = ""
		CHANGELOG = os.popen('git log {}..HEAD --oneline'.format(latestag)).read()
		chlg = "\n## CHANGELOG:\n"
		for x in CHANGELOG.split('\n')[:-1]:
			chlg+=f"[`{x[:7]}`](https://github.com/{data['git']['github']}/commits/{x[:7]}){x[7:]}\n"

		data['build']['release_notes'] = ''
		data['build']['release_notes'] +=input('One line release message:\n> ')
		print('Extended desciption: (ctrl+c to finish):')

		while True:
			try:
				data['build']['release_notes'] +='\n'+input('> ')
			except KeyboardInterrupt:
				print('\n\n')
				break
		data['build']['release_notes']+=chlg if len(chlg.split('\n'))>4 else ''
		f = open('.release-notes-latest','w+')
		f.write(data['build']['release_notes'])
		f.close()
		data['build']['release_notes'] = data['build']['release_notes'].replace('\n',' / ').replace('"','`')[3:]

	try:
		version = data['latest_build'] = data['latest_build'].split('+')[0]
	except:
		print('You must run `sailboat build` first.')
		exit()
	if "pypi" in ids or len(ids)==1:
		print("Please make sure that you have a https://pypi.org/ account.")
		try:
			import twine
		except:
			input('Press enter to continue installing `twine`. Press ctrl+c to exit.')
			os.system('python3 -m pip install --user --upgrade twine || python3 -m pip install --upgrade twine')
			import twine
		del twine
		print('\u001b[4m\u001b[1;36mPyPi Credentials:\u001b[0m')
		os.system('python3 -m twine upload dist'+os.sep+'pypi'+os.sep+'*')
		print('waiting...')
	if "brew" in ids or len(ids)==1:
		if "pypi" in runs:
			print('Must wait 20 seconds for pypi files to upload before creting homebrew formula...\n')
			for i in range(0, 20):
					time.sleep(1)
					sys.stdout.write(u"\u001b[1000D" + str(20-(i + 1)).zfill(2) + " seconds left.\t")
					sys.stdout.flush()
			print()
		try:
			shutil.rmtree('homebrew-taps')
		except:
			pass
		if data['build']['homebrew']:
			f = open('dist'+os.sep+'homebrew'+os.sep+data['name']+'.rb')
			oldFormula = f.read()
			f.close()
			f = open('dist'+os.sep+'homebrew'+os.sep+data['name']+'.rb','w+')
			req = requests.get('https://pypi.org/pypi/{}/json'.format(data['short_name'])).json()
			versionPy = req['info']['version']
			url = req['releases'][versionPy][0]['url']
			sha256 = req['releases'][versionPy][0]['digests']['sha256']
			if not (url.endswith('.tar.gz') or url.endswith('.zip')):
				try:
					url = req['releases'][versionPy][1]['url']
					sha256 = req['releases'][versionPy][1]['digests']['sha256']
				except:
					url = "error"
					sha256 = "error"
			f.write(oldFormula.format(pyhosted=url,sha256=sha256,version=versionPy))
			f.close()
			if ('-d','') in arguments:
				input('waithing for user input...')
			if 'github' in data['git']:
				uname = data['git']['github'].split('/')[0]
			else:
				uname = input('Your GitHub username: ')
			print('\u001b[4m\u001b[1;36mHomebrew Release:\u001b[0m')
			if 'brew' not in data['git'] and len(os.popen(f'git ls-remote https://github.com/{uname}/homebrew-taps').read())<4:
				print('Creating new repo')
				print('To create a homebrew formula, you must first setup a GitHub repository called "homebrew-taps".\n\nPlease go to https://github.com/new and create a repo called `homebrew-taps`.')
				input('Press enter when done.')
				os.mkdir('homebrew-taps')
				os.chdir('homebrew-taps')
				os.system(f'git init;echo "# homebrew-taps" >> README.md;git remote add origin https://github.com/{uname}/homebrew-taps.git')
				os.chdir('..')
			else:
				print('Cloning existing repo')
				os.system(f'git clone https://github.com/{uname}/homebrew-taps.git')
			if ('-d','') in arguments:
				input('waithing for user input...')
			shutil.copy('dist'+os.sep+'homebrew'+os.sep+data['name']+'.rb','homebrew-taps'+os.sep+data['name']+'.rb')
			os.system(f'cd homebrew-taps;git add .;git config --global credential.helper "cache --timeout=3600";git config user.name "{data["author"]}";git config user.email "{data["email"]}";git commit -F ..{os.sep}.release-notes-latest;git commit --amend -F ..{os.sep}.release-notes-latest;git tag v{version};git push origin master --tags;cd ..')
			data['git']['brew'] = uname+"/homebrew-taps"
		try:
			shutil.rmtree('homebrew-taps')
		except:
			pass
	if "github" in ids or len(ids)==1:
		if 'github' not in data["git"]:
			import sailboat.git
			sailboat.git.main()
		if data['build']['actions_built_latest']:
			up = 'git push origin master;'
		else:
			up = ''
		f = f'git add .;git config --global credential.helper "cache --timeout=3600";git config user.name "{data["author"]}";git config user.email "{data["email"]}";git commit -F .release-notes-latest;git commit --amend -F .release-notes-latest;git tag v{version};git remote add origin https://github.com/{data["git"]["github"]}.git || echo;echo "\u001b[4m\u001b[1;36mGitHub Credentials: (will be cached for 1hr)\u001b[0m";{up}git push origin master --tags;echo "--- done! ---"'
		if up!="":
			print('\n\nPushed twice to update workflow action before tagged push.')
		os.system(f)
		data['build']['actions_built_latest'] = False
		f = open('.'+os.sep+'sailboat.toml','w+')
		f.write(toml.dumps(data))
		f.close()

	print('\n\n\u001b[4m\u001b[1;36mRelease Overview:\u001b[0m')
	print('\nSuccesfully release version \u001b[34m'+version+'\u001b[0m!')
	print('\nView the latest stable releases at:')
	print('PyPi:   				https://pypi.org/project/'+data['short_name'])
	print('GitHub: 				https://github.com/'+data['git']['github'])
	print('GitHub(brew):	https://github.com/'+data['git']['brew'])
	
	