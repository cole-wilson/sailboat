---
title: About Plugins
layout: default
---
# About Plugins
Sailboat uses a plugin based architecture. Every single command or subcommand is a plugin, even the core features. Plugins are registered using the [Python entry points system](https://amir.rachum.com/blog/2017/07/28/python-entry-points/), using the group name `sailboat_plugins`. There are four types of plugins:
### `core`
This type of plugin is reserved for 1st party plugins - plugins that are part of the actual Sailboat source. They have unreserved access to all project data, and therefore this type should not be used in custom plugins.
### `command`
`command` plugins are most basic form of a plugin. They are called by typing `sail <name of plugin>`. They are standalone python scripts that add to the project, like a task list manager.
### `build`
This is perhaps the most common type of plugin, they are run with the `build` core plugin, and are used to generate or edit project files. An example would be the PyInstaller plugin, which generates frozen binaries of the project. These should store output in the top level `dist` folder, in a subfolder with the name of the project. For example: the PyInstaller plugin saves output in `./dist/pyinstaller`. Build plugins can also contain `release` plugins within them.
### `release`
This group of plugins is used by the `release` core plugin. They are used to distribute files. For example: the `homebrew` release plugin uploads the Homebrew formula to a GitHub repo.

All plugins should be a subclass of `sailboat.plugins.Plugin`, a basic class that provide the neccesary functions and registration features. An example `command` plugin might look like this:
```python
from sailboat.plugins import Plugin

class Echo(Plugin):
	description = "A basic command plugin that echos it's input."
	_type = 'command'
	setup = {"string_to_echo":"What string should I echo? "}  # Used by wizard
    
	def run(self):
		string = self.getData('string_to_echo')  # Get string to echo.
		print(string)
		return
```
Plugins store their data in the `sailboat.toml` file, under their type namespace. For example, the above example will store it's data like so:
```toml
...
[command.echo]
string_to_echo = "Testing..."
...
```
A plugin should ***NEVER*** edit the `sailboat.toml` file on it's own. Instead plugins should use the provided functions OR edit `self.data`, a dictionary of the file. Only data stored in the plugins namespace will be preserved. However, a plugin can read from the top level data.

## Registering Your Plugin:
All you have to do to register your plugin is add an entry point for it in `sailboat_plugins`. If you are using sailboat to build your project, this is easy, just edit `sailboat.toml`:
```toml
...
[build.pypi.entry_points.sailboat_plugins]
build = "sailboat.build:Build"  # name = your_module.your_file:Your_Class
...
```
## Variables:
The following top level variables are used in a plugin class. They can be accessed with `self.variable_name`.

### `_type`
One of `command`,`release`,`build`, or `core`. This tells the plugin manager when and how to run the plugin.
Default is `build`.

### `_show`
This is only for command plugins: if it is False, the command will not show in the help list. Default is True.

### `_release`
Only for build plugins. If the value is True, then the `release()` function is availible. This alows a build plugin to provide both a build script AND a release script. Default is False.

### `_order`
Only for release plugins. Higher numbers are run last. Two plugins that have the same number are sorted by name lexigraphically./= Default: 0.

### `_os`
For GitHub actions workflows. A space seperated string containing `windows`,`mac`, and/or `linux`. Default: `linux`

### `data`
This contains a dictionary with the contents of the `sailboat.toml` file. It is editable, however only data in the plugins namespace is persisted.

### `name`
The name that called the plugin.

### `description`
A description of the plugin. Default: `<no description provided>`

### `options`
A sys.argv like list of command line arguments. These are the arguments only for that plugin.

### `version`
For build plugins: the version being built/released in semver notation.

### `setup`
If `wizard()` is not defined, the core qizard plugin will use this to setup settings for the plugin in `sailboat.toml`.
It must be a dictionary with the syntax `data_key:question_to_ask_user`. If the key has `::` in it, the part after the `::` is converted to a type. (see example)
```python
# example
setup = {
	"number::int":"What number would you like to chose?"  # Keeps asking until int.
}
```
Valid types are: `[int,str,bool]` (bool=y/n)

## Functions:
The following functions are availible for plugin authors to use:

### `wizard()`
Runs at install, and when called with `sail wizard`.
If this is not defined, it runs the `setup` variable (see above). If it is defined, it runs the content of the function as a script.

### `add()`
Run at install.

### `run()`
Runs when a command plugin is run, or when a build plugin is run.

### `release()`
Called when release plugin is run, or when a build plugin with `_release = True` is run at release time.

### `storeData(key,value)`
Store key,value in plugin namespace

### `getData(key)`
Get key from plugin namespace

### `section(text)`
Returns text underlined, in bold cyan.

### `blue(text)`
Return blue text

### `red(text)`
Returns red text

### `getResource(filename,mode='r')`
Returns a `File` object of the filename relative to Plugin source.

### `getFiles(extension,recursive=True)`
Returns list of all files ending with extension.

