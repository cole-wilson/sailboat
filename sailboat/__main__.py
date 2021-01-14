import sys
import os
import pkg_resources
import toml
import json
import sailboat.plugins
import sailboat.core
from sailboat.build import Build
from pathlib import Path

try:
	path = Path(__file__)
	prefix = os.path.abspath(path.parent)+os.sep
except:
	prefix = os.path.dirname(os.path.abspath(__file__))+os.sep
# print(prefix)

# =============================================================================
__doc__ = "usage: sail [command]\n"
# =============================================================================
class echo(sailboat.plugins.Plugin):
	_type = "release"
	description = "say argv!"
	setup = {"int::int":"Integer test: "}
	def run(self):
		print(" ".join(self.options))

def refreshEntries():
	plugins={"core":{},"build":{},"release":{},"command":{}}
	for entry_point in pkg_resources.iter_entry_points(group='sailboat_plugins'):
		temp = entry_point.load()
		plugins[temp._type][entry_point.name] = {
			"show" : temp._show,
			"dist" : str(entry_point.dist).split(' ')[0],
			"description" : temp.description,
			"type" : temp._type,
			'release' : temp._release,
			"order" : temp._order,
			"default_os":temp._os
		}
	f = open(os.path.abspath(path.parent)+os.sep+'plugins.json','w+')
	f.write(json.dumps(plugins, indent=2, sort_keys=True))
	f.close()
	del f
	return plugins

def main():
	global __doc__
	opath = os.getcwd()
	while not os.path.isfile('sailboat.toml') and os.getcwd().count(os.sep)>2:
		os.chdir('..')
	if not os.path.isfile('sailboat.toml'):
		needswizard = True
		data = {}
		os.chdir(opath)
	else:
		needswizard = False
		with open('sailboat.toml') as file:
			data = toml.loads(file.read())
			if data == {}:
				needswizard = True
	
	if 'command' not in data:
		data['command'] = {}
	if 'build' not in data:
		data['build'] = {}
	if 'release' not in data:
		data['release'] = {}
	if 'git' not in data:
		data['git'] = {}
	

# =============================================================================
	plugins = json.loads(open(prefix+'plugins.json').read())

	if plugins=={} or (len(plugins.keys())!=4):
		plugins = refreshEntries()


	if len(plugins['core'].keys())!=0:
		__doc__+="\n\tcore commands:"

	for command in plugins['core'].keys():
		if plugins['core'][command]['show']:
			__doc__+="\n\t\t- \u001b[36;1m"+command+"\u001b[0m: "+plugins['core'][command]['description'].capitalize()

	__doc__+="\n\t\t- \u001b[36;1mhelp\u001b[0m: display this message."

	if len(plugins['command'].keys())!=0:
		__doc__+="\n\n\tother commands:"

	for command in plugins['command'].keys():
		if plugins['command'][command]['show'] and command in data['command']:
			__doc__+="\n\t\t- \u001b[36;1m"+command+"\u001b[0m: "+plugins['command'][command]['description'].capitalize()

	__doc__+="\n"

# =============================================================================

	if len(sys.argv) < 2:
		print(__doc__)
		return
	if needswizard:
		command = 'wizard'
	else:
		command = sys.argv[1]
	if command == 'help':
		print(__doc__)
		return

	if command in plugins['core']:
		t = 'core'
	elif command in plugins['command']:
		t = 'command'
	else:
		print('sailboat: error: {} is not a valid command. Please make sure you have installed it.'.format(command))
		return	

	if t!='core' and command not in data['build'] and command not in data['release'] and command not in data['command']:
		print('sailboat: error: {} *is* a valid command, but it isn\'t installed on this project. Install it with the `add` command.'.format(command))
		return

	dist = plugins[t][command]['dist']
	temp = pkg_resources.load_entry_point(dist,'sailboat_plugins',command)
	temp = temp(
		data=data,
		options=sys.argv[2:],
		name=command,
	)
	if t == "core":
		temp.run(plugins=plugins)
	else:
		temp.run()

	if t == 'core':
		data = temp.data
	else:
		data[t][command] = temp.data[t][command]

	basic_data = {}
	resources = {'resources':{}}
	commands = {'command':{}}
	builds = {'build':{}}
	release = {'release':{}}
	other = {}

	with open('sailboat.toml','w+') as f:
		for key in data.keys():
			if not isinstance(data[key],dict):
				basic_data[key] = data[key]
			elif key == 'resources' and len(data[key].values())>0:
				resources['resources'] = data[key]
			elif key == 'command' and len(data[key].values())>0:
				commands['command'] = data[key]
			elif key == 'build' and len(data[key].values())>0:
				builds['build'] = data[key]
			elif key == 'release' and len(data[key].values())>0:
				release['release'] = data[key]
			elif key not in ('build','release','command','resources'):
				other[key] = data[key]
		resources  = resources if resources != {'resources':{}} else {}
		commands  = commands if commands != {'command':{}} else {}
		builds  = builds if builds != {'build':{}} else {}
		release  = release if release != {'release':{}} else {}
		other  = other if other != {'other':{}} else {}
		o = [*map(toml.dumps,[basic_data,resources,commands,builds,release,other])]
		out="""#	  _____       _ _ _                 _     
#	 / ____|     (_) | |               | |  _ 
#	| (___   __ _ _| | |__   ___   __ _| |_(_)
#	 \___ \ / _` | | | '_ \ / _ \ / _` | __|  
#	 ____) | (_| | | | |_) | (_) | (_| | |_ _ 
#	|_____/ \__,_|_|_|_.__/ \___/ \__,_|\__(_)
                                          
# Basic Setup:
{}

# Resource Setup:
{}

# Plugin Commands:
{}

# Build Routines:
{}

# Release Routines:
{}

# Other:
{}

# Thank you for using Sailboat!"""
		out = out.format(o[0],o[1],o[2],o[3],o[4],o[5])
		f.write(out)

if __name__ == "__main__":
	main()