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
		else:
			data['git']['github']=''
	open('.'+os.sep+'sailboat.toml','w+').write(toml.dumps(data))