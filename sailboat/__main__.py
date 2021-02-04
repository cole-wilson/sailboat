import sys
import os
import pkg_resources
import toml
import json
import sailboat.plugins
import sailboat.core
import colorama
colorama.init()  # For Windows

prefix = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + os.sep

__doc__ = "usage: sail [options ...] [command]\n"

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
			"default_os":str(temp._os)
		}
	f = open(prefix + 'plugins.json','w+')
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
	needswizard =False
	if 'command' not in data:
		data['command'] = {}
	if 'build' not in data:
		data['build'] = {}
	if 'release' not in data:
		data['release'] = {}
	if 'git' not in data:
		data['git'] = {}

	switches = []
	startindex = 0
	for index,value in enumerate(sys.argv[1:]):
		if value.startswith('--'):
			switches.append(value[2:])
		elif value.startswith('-'):
			switches.extend(value[1:])
		else:
			startindex = index
			break
	options = [sys.argv[0],*sys.argv[1:][startindex:]]

# =============================================================================
	plugins = json.loads(open(prefix+'plugins.json').read())

	if 'v' in switches or 'version' in switches:
		print('Sailboat version {}\n\nHelp:\ncontact cole@colewilson.xyz'.format(sailboat.__version__))
		sys.exit(0)
	if 'refresh' in switches or 'r' in switches or plugins=={} or (len(plugins.keys())!=4):
		plugins = refreshEntries()
		print('reloaded plugins')

	a_commands = []

	if len(plugins['core'].keys())!=0:
		__doc__+="\n\tcore commands:"

	for command in plugins['core'].keys():
		if plugins['core'][command]['show']:
			__doc__+="\n\t\t- \u001b[36;1m"+command+"\u001b[0m: "+plugins['core'][command]['description'].capitalize()
			a_commands.append(command)

	__doc__+="\n\t\t- \u001b[36;1mhelp\u001b[0m: Display this message."

	if len(plugins['command'].keys())!=0:
		__doc__+="\n\n\tother commands:"

	for command in plugins['command'].keys():
		if plugins['command'][command]['show'] and command in data['command']:
			__doc__+="\n\t\t- \u001b[36;1m"+command+"\u001b[0m: "+plugins['command'][command]['description'].capitalize()
			a_commands.append(command)

	__doc__+="\n"

# =============================================================================

	if len(options) < 2:
		print(__doc__)
		return
	if needswizard:
		command = 'wizard'
	else:
		command = options[1]
	autocomplete = False
	if command == 'help' or 'help' in switches or 'h' in switches:
		print(__doc__)
		return

	if command in plugins['core']:
		t = 'core'
	elif command in plugins['command']:
		t = 'command'
	else:
		if not autocomplete:
			print('sailboat: error: {} is not a valid command. Please make sure you have installed it.'.format(command))
		return

	if t!='core' and command not in data['build'] and command not in data['release'] and command not in data['command']:
		print('sailboat: error: {} *is* a valid command, but it isn\'t installed on this project. Install it with the `add` command.'.format(command))
		return

	dist = plugins[t][command]['dist']
	temp = pkg_resources.load_entry_point(dist,'sailboat_plugins',command)
	temp = temp(
		data=data,
		options=options[2:],
		name=command,
		prefix=prefix
	)
	if autocomplete:
		print(" ".join(temp.autocomplete()))
	elif t == "core":
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
		out="""#            _  _  _                _   
#  ___ __ _ (_)| || |__  ___  __ _ | |_ 
# (_-</ _` || || || '_ \/ _ \/ _` ||  _|
# /__/\__,_||_||_||_.__/\___/\__,_| \__|
                                      
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
		if '_comments' in data and not data['_comments']:
			print()
			out = "{}\n{}\n{}\n{}\n{}\n{}\n"
		out = out.format(o[0],o[1],o[2],o[3],o[4],o[5])
		f.write(out)

if __name__ == "__main__":
	main()