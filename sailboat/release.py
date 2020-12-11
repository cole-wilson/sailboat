# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import sys
import toml

def main(arguments,ids):
	if not os.path.isfile('.'+os.sep+'sailboat.toml'):
		print('Please create a config file with `sailboat wizard` first.')
		sys.exit(0)
	try:
		data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
	except toml.decoder.TomlDecodeError as e:
		print('Config error:\n\t'+str(e))
		exit()
	data['build']['release_notes'] = ''
	data['build']['release_notes'] +=input('One line release message:\n> ')
	print('Extended desciption: (ctrl+c to finish):')

	while True:
		try:
			data['build']['release_notes'] +='\n'+input('> ')
		except KeyboardInterrupt:
			print('\n\n')
			break
	f = open('.release-notes-latest','w+')
	f.write(data['build']['release_notes'])
	f.close()
	data['build']['release_notes'] = data['build']['release_notes'].replace('\n',' / ').replace('"','`')[3:]

	try:
		version = data['latest_build']
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
		os.system('python3 -m twine upload dist'+os.sep+'pypi'+os.sep+'*'+' -c "'+data['build']['release_notes']+'"')
	if "github" in ids or len(ids)==1:
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