__version__ = "0.26.2"  # Added by Sailboat

import os
import glob
import sys
import json
import blessed


class Plugin:
    """
	The basic sailboat Plugin class
	"""
    name = ""
    data = {}
    description = "<no description provided>"
    version = ""
    options = []
    setup = {}
    _type = "build"
    _show = True
    _release = False
    _order = 0
    _os = 'linux'
    autocompletion = {}

    def registerAutocompletion(self):
        import __main__
        prefix = self.prefix
        f = open(prefix + "autocomplete", 'a')
        for x in self.autocompletion.keys():
            f.write(x + "::" + self.autocompletion[x] + "\n")

    def release(self):
        pass

    def init(self):
        pass

    def add(self):
        print('Installing...')

    def __repr__(self):
        return "<sailboat plugin: " + self.name + ">"

    def __init__(self, data=None, options=None, prefix=__file__, name=None, version=None):
        if options is not None:
            self.options = options
        if version is not None:
            self.version = version
        if data is not None:
            self.data = data
        self.name = name
        self.prefix = prefix
        self.init()
        self.term = blessed.Terminal()

    def storeData(self, key, value):
        if self._type == "core":
            self.data[key] = value
        else:
            if self.name not in self.data[self._type]:
                self.data[self._type][self.name] = {}
            self.data[self._type][self.name][key] = value

    def section(self, string):
        if sys.platform.startswith('win'):
            return string
        else:
            return self.term.cyan + self.term.underline + str(string) + self.term.normal + self.term.nounderline

    def blue(self, string):
        if sys.platform.startswith('win'):
            return string
        else:
            return self.term.blue + self.term.bold + str(string) + self.term.normal

    def red(self, string):
        if sys.platform.startswith('win'):
            return string
        else:
            return self.term.red + str(string) + self.term.normal

    @property
    def data2(self):
        return self.data[self._type][self.name]

    def getData(self, key=None):
        try:
            if key == None:
                return self.data[self._type][self.name]
            return self.data[self._type][self.name][key]
        except BaseException as e:
            print('Error in {}:\n\t{}'.format(self.name, e))
            return None

    def getResource(self, name, rwmode='r'):
        prefix = os.path.dirname(os.path.abspath(__file__)) + os.sep
        return open(prefix + name, rwmode)

    def wizard(self, setup_dict=None):
        if setup_dict == None:
            setup_dict = self.setup
        for key in setup_dict.keys():
            try:
                t = "::".join(key.split('::')[1:])
                key = key.split('::')[0]
            except:
                t = 'str'
            if self._type != "core" and self.name in self.data[self._type] and key in self.data[self._type][self.name]:
                print(self.blue(setup_dict[str(key) + "::" + t]) + " " + str(self.data[self._type][self.name][key]))
            elif self._type == "core" and key in self.data:
                print(self.blue(setup_dict[key + "::" + t]) + self.data[key])
            elif t == "str":
                self.storeData(key, input("\u001b[34m" + setup_dict[key + "::" + t] + " \u001b[0m"))
            elif t == "int":
                while True:
                    try:
                        self.storeData(key, int(input("\u001b[34m" + setup_dict[key + "::" + t] + " \u001b[0m")))
                        break
                    except ValueError:
                        print('Please provide an integer.')
            elif t == "bool":
                try:
                    self.storeData(key, input("\u001b[34m" + setup_dict[key + "::" + t] + " [y/n] \u001b[0m")[0] == 'y')
                except:
                    print('error: you did not supply a value!')
                    self.storeData(key, input("\u001b[34m" + setup_dict[key + "::" + t] + " [y/n] \u001b[0m")[0] == 'y')
            else:
                self.storeData(key, input("\u001b[34m" + setup_dict[key + "::" + t] + " \u001b[0m"))
        return self.data

    def getFiles(self, extension, recursive=True):
        if recursive:
            files = []
            for root, dirs, files in os.walk('.'):
                for filename in files:
                    if filename.endswith(extension):
                        files.append(root + filename)
            return files
        else:
            return list(glob.glob(extension))

    def run(self, **kwargs):
        print(
            'This plugin has not been set up correctly.\nIf you are the developer, please add a run(self,**kwargs) function to your class.')
        return


class PluginNotFound(Exception):
    """Raised when a sailboat plugin was not found."""
    pass


def refresh_plugins() -> dict:
    """
	Refresh the plugins.json file where plugin information is kept.
	A dict of the updated plugins is returned.
	"""

    plugins = {"core": {}, "build": {}, "release": {}, "command": {}}
    from pkg_resources import iter_entry_points
    entry_points = iter_entry_points(group='sailboat_plugins')
    for entry_point in entry_points:
        temp = entry_point.load()
        plugins[temp._type][entry_point.name] = {
            "show": temp._show,
            "dist": str(entry_point.dist).split(' ')[0],
            "description": temp.description,
            "type": temp._type,
            'release': temp._release,
            "order": temp._order,
            "default_os": temp._os
        }
    prefix = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + os.sep
    with open(prefix + 'plugins.json', 'w+') as pluginfile:
        # pluginfile.write(json.dumps(plugins, indent=2, sort_keys=True))  # Pretty Printed
        pluginfile.write(json.dumps(plugins))  # Minified
    return plugins


def get_plugin(plugin_name: str, plugin_type: str = None) -> Plugin:
    """
	Returns a tuple of (plugin type, plugin) with the given plugin_name.
	If plugin_type is None, then the first plugin match is used.
	If a plugin is not found then a PluginNotFound exception is raised.
	"""

    prefix = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + os.sep
    with open(prefix + 'plugins.json', 'r') as pluginfile:
        plugins = json.loads(pluginfile.read())

    if plugin_type == None:
        if plugin_name in plugins['core']:
            plugin_type = 'core'
        elif plugin_name in plugins['build']:
            plugin_type = 'build'
        elif plugin_name in plugins['command']:
            plugin_type = 'command'
        elif plugin_name in plugins['release']:
            plugin_type = 'release'
        else:
            raise PluginNotFound('The plugin `{}` could not be found.'.format(plugin_name))

    distribution = plugins[plugin_type][plugin_name]['dist']
    from pkg_resources import load_entry_point
    plugin = load_entry_point(distribution, 'sailboat_plugins', plugin_name)
    return (plugin_type, plugin)
