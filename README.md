# sailboat

![Publish system files for Sailboat.](https://github.com/cole-wilson/sailboat/workflows/Publish%20system%20files%20for%20Sailboat./badge.svg)

A quick and easy way to distribute your python projects!

sailboat will let you go from hello world to a published app in about 5 minutes!
It generates a setup.py and correct directory structure for you in seconds, all with a simple config file.

In addition to this, it can build your Mac and Windows apps in the cloud using GitHub actions, so you don't need to have both a Mac and Windows computer to create apps. To use this feature, activate it with the wizard. 

Please see the [quickstart](#quickstart) for an example.
## Installation
**Install with Pip:** `pip3 install sailboat`
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
 
 - `-y`: No interaction, always accept changes.
 
 - `--actions-only`: Only generate actions file.
 
 - `--mac-only`: Only generate mac file.
 
 - `--windows-only`: Only generate windows file.
 
 - `--pypi-only`: Only generate pypi files.

 - `--setup-only`: Only generate setup.py.
 
 - `--no-installer`: Overide installer config.
> *These options can be combined*


### `sailboat release [pypi | github]`
This will upload your built project to PyPi and GitHub. *(or just one of them, depending on the command options)*
## Quickstart
Let's say that we have a file `helloworld.py`:
```python3
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
