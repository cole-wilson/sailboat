# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import toml

def main():
	try:
		data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
	except toml.decoder.TomlDecodeError as e:
		print('Config error:\n\t'+str(e))
		exit()
	if data['git']=={}:
		if input('Setup git repo? [y/n] ')[0]=='y':
			al = input('What is your GitHub repo? (leave blank if you don\'t have one yet.)\n<user>/<repo_name>: ')
			if al=="":
				print('Goto https://github.com/new and create a repo called "'+data['short_name']+'."')
				input('Press enter when done.')
				user = input('What is your GitHub username? ')
				al = user+"/"+data['short_name']
			os.system(f'git init;git config --global credential.helper "cache --timeout=3600";git config user.name "{data["author"]}";git config user.email "{data["email"]}";git add .;git commit -m ":rocket: Initial Commit!";git remote add origin https://github.com/{al}.git;git push -u origin master;')
			data['git']['github']=al
		else:
			data['git']['github']=''
	else:
		print('Already set up.')
	open('.'+os.sep+'sailboat.toml','w+').write(toml.dumps(data))