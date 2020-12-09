import os
import sys
import toml

def main(arguments,ids):
	if not os.path.isfile('.'+os.sep+'sailboat.toml'):
		print('Please create a config file with `sailboat wizard` first.')
		sys.exit(0)
	with open('.'+os.sep+'sailboat.toml') as datafile:
		data = toml.loads(datafile.read())
	data['build']['release_notes'] = ''
	print('Please provide a summary of the changes (ctrl+c to finish):')
	while True:
		try:
			data['build']['release_notes'] +='\n'+input('> ')
		except KeyboardInterrupt:
			print('\n\n')
			break
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
		f = f'git add .;git config --global credential.helper "cache --timeout=3600";git config user.name "{data["author"]}";git config user.email "{data["email"]}";git commit -m "{data["build"]["release_notes"]}";git commit --amend -m "{data["build"]["release_notes"]}";git tag v{version};git remote add origin https://github.com/{data["build"]["github"]}.git || echo;echo "\u001b[4m\u001b[1;36mGitHub Credentials: (will be cached for 1hr)\u001b[0m";{up}git push origin master --tags;echo "--- done! ---"'
		if up!="":
			print('\n\nPushed twice to update workflow action before tagged push.')
		os.system(f)
		data['build']['actions_built_latest'] = False
		f = open('.'+os.sep+'sailboat.toml','w+')
		f.write(toml.dumps(data))
		f.close()