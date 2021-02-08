<h1 align="center"><img src="https://www.pinclipart.com/picdir/big/383-3832964_im-on-a-boat-stamp-sailboat-stencil-clipart.png" width="70px">
<br>
sailboat
<br>
<a href="https://github.com/cole-wilson/sailboat"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/cole-wilson/sailboat?style=social"></a>
<a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fsole-wilson%2Fsailboat"><img alt="Twitter" src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fsole-wilson%2Fsailboat"></a>
<br>
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/cole-wilson/sailboat">
<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/cole-wilson/sailboat?label=latest%20release">
<img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/cole-wilson/sailboat/Publish%20release%20files%20for%20Sailboat.">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/cole-wilson/sailboat">
<img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/cole-wilson/sailboat?include_prereleases">
<img alt="GitHub" src="https://img.shields.io/github/license/cole-wilson/sailboat">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/sailboat">

</h1>

<a style="display:inline-block;" align="center" href="//sailboat.colewilson.xyz">View Documentation Site</a>

## About
Sailboat is a Python developer's best friend. It's a Python build tool that can do anything you need it to! It suports a countless number of plugins — you can even [make your own](#plugins). Sailboat is made for anyone, whether you are a beginner on your very first project, or a senior software engineer with years of experience. 

Let's say that that you have created a basic game, **Guess My Number**, and you want to send it to all of your friends. There are a lot of different ways you can do this, but using Sailboat is the easiest. All you have to do is type three commands: `sail quickstart`, `sail build`, and `sail release`, and you can have a Homebrew file, a `pip` installable package, and a [PyInstaller](https://www.pyinstaller.org/) desktop app. So easy!

Sailboat also supports custom subcommands. These don't build your project, but they can add features such as a todo list that help speed up your development process.

## Installation
### Pip:
```bash
pip3 install sailboat
```
### Binary:
Download from [latest release](https://github.com/cole-wilson/sailboat/releases/latest).
### Homebrew:
```bash
brew install cole-wilson/taps/Sailboat
```
### Build From Source:
```bash
git clone https://github.com/cole-wilson/sailboat
cd sailboat
python3 setup.py install
```
## Usage:
Sailboat is intended to be used from the command line/terminal.

It is suggested to run `sail quickstart` to get started. Then, use `sail build` to build your project, and `sail release` to release it! Be sure to to look at the subcommand docs for more detail. 
*(look in table below)*

There are two base commands that can be used: `sail` and `sailboat`. These both do exactly the same thing, there is no difference. `sail` will be used in the documentation, as it's shorter easier to type, but you can do whatever.

To get a list of the availible subcommands type `sail help`.
To refresh the plugin list, type `sail -r`.

There are countless subcommands, but these are the core ones:

|subcommand|description|
|----------|-----------|
|	add | Add a plugin to your project. |
|	build | Build your project for release. |
|	dev | Run your project without building it. |
|	git | Manage git for your project. |
|	github | Manage git for your project. |
|	plugins | Plugin manager. |
|	quickstart | Get your project up and running. |
|	release | Release your project. |
|	remove | Remove a plugin from you project. |
|	wizard | Configure you project or a plugin. |
|	workflow | Generate a GitHub actions workflow file. |
|	help | Display this message. |

## Plugins:
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

Plugins can get very complex, and therefore useful, but it is too long to put here. Please look at the [`sailboat.colewilson.xyz/plugins.html`](//sailboat.colewilson.xyz/plugins.html) file for details.

## Acknowledgements:
Thanks to all the people at PyInstaller, dmgbuild, twine, and GitHub actions who provided ways for me to create this. 

## Stargazers
[![Stargazers repo roster for @cole-wilson/sailboat](https://reporoster.com/stars/cole-wilson/sailboat)](https://github.com/cole-wilson/sailboat/stargazers)


## Contributors
 - Cole Wilson
 
## Contact
Please submit an issue if you have any questions or need help or find a bug. I'm happy to help!

<cole@colewilson.xyz>
