import os
import glob
import toml
import sys
import shutil

questions = {
	"name":"Full name of project",
	"short_name":"Short name of project",
	"author":"Your name(s)",
	"email":"Project email",
	"short_description":"Short description of your project",
	"description":"Full description of your project",
	"url":"Main project URL",
	"license":"License",
	"keywords":"Keywords seperated with a space",
	"data_files":"Data files (with *) to include in project seperated with a space",
	"file":"Main python file, leave blank for no main file",
	"modules":"Required modules, seperated with space"
}
questions2= {
	"type":"Please choose one of the following options for your project:\n\t1. My project only deals with text (not graphical).\n\t2. My project is a graphical app.\n>>>",
	"mac":"Would you like to distribute a Mac app for your project? [y/n]",
	"windows":"Would you like to distribute a Windows app for your project? [y/n]",
}


def main():
	"""
	The setup wizard for sailboat
	"""
	prefix = os.path.dirname(os.path.abspath(__file__))+os.sep+'resources'
	data = {}
	if os.path.isfile('.'+os.sep+'sailboat.toml'):
		data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
	print("I'm going to ask you a few questions about your project to create a config file!\n\nPlease fill in everything to your ability. If you can't provide a value, leave it blank.\n")
	for key in questions:
		if key not in data:
			if len(glob.glob('.'+os.sep+'LICENS*'))>0 and key=="license":
				print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
				for license in "AGPL-3.0/Apache-2.0/BSD-2-Clause/BSD-3-Clause/GPL-2.0/GPL-3.0/LGPL-2.1/LGPL-3.0/MIT".split(os.sep+''):
					print(f'\t- {license}')
				data[key] = input(">>>\033[0m ")
			elif len(glob.glob('.'+os.sep+'LICENSE*'))==0 and key=="license":
				data[key]=""
			elif key=="data_files" or key=="modules":
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ").split(' ')
				data[key] = list(filter(None, data[key]))

			else:
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ")
		else:
			print("\033[1;34m"+str(questions[key])+":\033[0m "+str(data[key]))
	if "build" not in data:
		data['build']={}
	data['fullname']=data['name']
	
	for key in questions2:
		if key not in data['build']:
			c=input("\033[1;34m"+questions2[key]+"\033[0m ")
			data['build'][key] = c[0]=='y' if '[y/n]' in questions2[key] else c
		else:
			print("\033[1;34m"+str(questions2[key])+"\033[0m "+str(data['build'][key]))
	if (data['build']['mac'] or data['build']['windows']):
		if 'installer' in data['build']:
			print("\033[0m"+"Would you like to provide an installer for the app(s)? (recomended) [y/n]"+"\033[0m "+str(data['build']['installer']))
		else:
			data['build']['installer'] = True if input("\033[1;34m"+"Would you like to provide an installer for the app(s)? (recomended) [y/n]"+"\033[0m ")[0]=="y" else False
	if (not data['build']['mac'] and not data['build']['windows']):
		data['build']['installer'] = False
	if not sys.platform.startswith('win') and data['build']['windows']:
		print('\033[1;31mYou can only make a Windows app on a Windows computer.\033[0m')
		needswin=True
	else:
		needswin=False
	if sys.platform != 'darwin' and data['build']['mac']:
		print('\033[1;31mYou can only make a Mac app on a Mac.\033[0m')
		needsmac=True
	else:
		needsmac=False

	if (needsmac or needswin):
		if ('actions' in data['build']):
			print('\033[1;34mGithub Actions can build your app on the cloud for free.\n\033[1;31mWould you like to use that to build your apps? [y/n] \033[0m'+str(data['build']['actions']))
			actions = data['build']['actions']
		else:
			actions = True if input('\033[1;34mGithub Actions can build your app on the cloud for free.\n\033[1;31mWould you like to use that to build your apps? [y/n] \033[0m')[0] == 'y' else False
			data['build']['actions'] = actions
	else:
		actions = False
		data['build']['actions'] = False
	if actions:
		try:
			f = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml','w+')
		except:
			os.system('mkdir -p .github'+os.sep+'workflows'+os.sep)
			f = open('.github'+os.sep+'workflows'+os.sep+'sailboat.yml','w+')
		f.write(open(prefix+os.sep+'sailboat.yml.template').read())
		if 'github' not in data['build']:
			ghrepo = True if input('\033[1;34mDo you have a GitHub repo for this project yet? [y/n] \033[0m')[0] == 'y' else False
			if not ghrepo:
				create = True if input('\033[1;34mWould you like me to create one? (strongly recommended) [y/n] \033[0m')[0] == 'y' else False
				if create:
					print('\033[1;31mGo to https://github.com/new and create a repo called `'+data['short_name']+'`. When you\'ve done that, come back here and push enter.\033[0m')
					input('')
					ghusername = input("\033[1;34mYour github username: \033[0m")
					data['build']['github'] = ghusername+"/"+data['short_name']
					os.system(f'git init;git config user.name "{data["author"]}";git config user.email "{data["email"]}";git add .;git commit -m ":rocket: Initial Commit!";git remote add origin https://github.com/{ghusername}/{data["short_name"]}.git;git push -u origin master;')
				else:
					print('\033[1;31mOk!\033[0m')
					data['build']['github'] = 'N/A'
					print('\033[1;31m\nI have created the neccesary files in your project. Please upload this folder to GitHub to use this feature.\n\n\033[0mFor help, see https://docs.github.com/en/free-pro-team@latest/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line\033[0m')
			else:
				data['build']['github'] = input('\033[1;34mWhat is your repo? (user/repo): \033[0m')
				print('\033[1;31m\nI have created the neccesary files in your project. Please upload this folder to GitHub to use this feature.\n\n\033[0mFor help, see https://docs.github.com/en/free-pro-team@latest/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line\033[0m')
		else:
			print('\033[1;34mDo you have a GitHub repo for this project yet? [y/n] \033[0my')
	if os.path.isfile('README.md'):
		if input('\033[1;34mOverwrite current README.md? [y/n]\033[0m ')[0]=='y':
			open('README.md','w+').write(open(prefix+os.sep+'readme.template').read().format(**data))
	else:
		open('README.md','w+').write(open(prefix+os.sep+'readme.template').read().format(**data))
	if 'bundle_id' not in data['build']:
		data['build']['bundle_id'] = f"com.{data['author'].lower().replace(' ','')}.{data['short_name']}"
	if 'homebrew' not in data['build']:
		data['build']['homebrew'] = False
	if 'icon' not in data:
		data['icon'] = ''
	data['name']=data['name'].replace(' ','_').replace('/','-')
	f = open('.'+os.sep+'sailboat.toml','w+')
	f.write(toml.dumps(data))
	f.close()

	print('\n\n\033[1;31m`sailboat.toml` has been created. Please edit that for further changes and advanced options.\033[0m')