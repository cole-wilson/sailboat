

<h1 align="center"><img src="https://www.pinclipart.com/picdir/big/383-3832964_im-on-a-boat-stamp-sailboat-stencil-clipart.png" width="70px">
<br>
sailboat
<br>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/cole-wilson/sailboat?style=social">
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

Sailboat is a tool that drastically speeds up your Python development. It suports a countless number of plugins — you can even [make your own](#plugins).

Please see the [quickstart](#quickstart) for an example.
## Installation
**Install with Pip:** `pip3 install sailboat`
**Download Binary:** Download from [latest release](https://github.com/cole-wilson/sailboat/releases/latest).
**Homebrew:** `brew install cole-wilson/taps/Sailboat`

## Usage:
> **Note:** `sailboat` can be substituted for `sail` at any time.

It is suggested that you run `sailboat wizard` to get started.
### `sailboat wizard`
This command runs a setup wizard that generates a `sailboat.toml` file in your current directory.
It will also help you set up GitHub actions and creat a git repo.
### `sailboat dev`
This command lets you test your project on your own system without needing to install it every time.

(running `sailboat build` also does this)

### `sailboat git`

Setup git and GitHub.

### `sailboat [--options] build <version>`
This command is where everything happens! There are several things that `build` does with the given version:
1. First, it will build a directory structure that looks something like this.
```
.
├── .github
│   └── workflows
│       └── sailboat.yml
├── bin
│   └── <compiled .sh files for your project>
├── build
│   └── <location where build data is generated>
├── dist
│   └── <compiled files ready for distribution>
├── <project name>
│   ├── # This is where your source code goes:
│   ├── __init__.py
│   ├── __main__.py
│   ├── mod1.py
│   ├── mod2.py
│   ├── data.txt
│   └── etc...
├── .gitignore
├── LICENSE
├── README.md
├── setup.py
└── sailboat.toml
```
2. Generate GitHub Actions workflow files
3. Generate `.app`, `.dmg`, `.exe`, `.msi` files *(depending on your configuration and system)*
4. Generate files used for PyPi distribution.
#### Options:
Some valid commandline options are:
 
 - `-y`: No interaction, always accept changes. (BUILD MODE)
 
 - `--actions-only`: Only generate actions file. (BUILD MODE)
 
 - `--mac-only`: Only generate mac file. (BUILD MODE)
 
 - `--windows-only`: Only generate windows file. (BUILD MODE)
 
 - `--pypi-only`: Only generate pypi files. (BUILD MODE)

 - `--setup-only`: Only generate setup.py. (BUILD MODE)
 
 - `--no-installer`: Overide installer config. (BUILD MODE)

 - `-f`: Use `.release-notes-latest` file for release notes. (RELEASE MODE)
> *These options can be combined*


### `sailboat release [pypi | github]`
This will upload your built project to PyPi and GitHub. *(or just one of them, depending on the command options)*

## Configuration
There are several options in the configuration that are not mentioned in the wizard. This section explains what they do:

### `build.build_script`:
This option can provide a file name for custom pre and post build scripts for custom actions.
An example value would be `build.py`. 
Inside `build.py` you need one or two functions called `pre` and `post`.
Each one of these must have two positional arguments: `version` and `data`.
`version` is a string of the version triggering the build, and `data` is a `dict` containing the decoded `sailboat.toml` data.
If `data` is returned at the end of the function, it is used instead of the normal value, and is saved at the end of the build.
An example file might look like this:
```python
def pre(version,data):
	print("Building version {}".format(version))
def post(version,data):
	data['test'] = version
	return data
```
This file would run `pre()` at the beginning, and `post()` at the end. `data['test']` will be saved in `sailboat.toml`.

### `build.bundle_id`:
The OSX Bundle Identifier used in PyInstaller. Defaults to `com.<author>.<short_name>`.

### `build.actions_built_latest`:
Whether or not the GitHub actions file was changed at the last build, updates automatically.

### `latest_build`:
The latest built version.

### `resources.no_import`:
Modules found in `*.py` files that do *NOT* need to be required.


### `git.github`:
The upstream URL for `sailboat git` and `sailboat release`.

### `setup_data`:
This is a dictionary for custom `setup.py` values. For example:
```toml
[setup_data]
test = "test_value"
```
add the key `test` to `setup.py` with the value `"test_value"`;

## Quickstart
Let's say that we have a file `helloworld.py`:
```python
name = input("What's your name? ")
print(f"Hello {name}!")
```
That's all fine and good, but how will we distribute our awesome app so that all ou relatives and friends can run it?

Whenever you have this problem, there are normally two solutions:
 - Get everyone to install Python, and then distribute copies of your source code.


 - Go through the trouble of packaging and distributing your project as a native application.


Both of these are less than ideal, but with `sailboat` there is a third option:
	
 - Use sailboat to distribute your project to PyPi, and also generate native applications and installers in about 5 minutes!
  
    - To do this we will need to install `sailboat`: `pip3 install sailboat`

    - Next, we will have to generate a `sailboat.toml` file by running `sailboat wizard`.
  
    - After we have done this, just type `sailboat build 0.0.1` and wait for the build process to finish.

    - Next, we have to get a PyPi account. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/) to register.

    - After that, just type in `sailboat release` to finish!
    
    - Now, you can install your app by typing `pip3 install <your-app-name>` and run it with `<your-app-name>` if you have Python, or by launching the packaged app in the `./dist/pyinstaller/` folder.

## Acknowledgements:
Thanks to all the people at PyInstaller, dmgbuild, Wix.Py, twine, and GitHub actions who provided ways for me to create this. 

## Contributors
 - Cole Wilson
## Contact
<cole@colewilson.xyz>
