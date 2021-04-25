#!/usr/bin/env python3

# +------------------------+			   
# | Created with Sailboat  |
# |                        |
# | Do not edit this file  |
# | directly. Instead  	   |			   
# | you should edit the	   |			   
# | `sailboat.toml` file.  |			   
# +------------------------+	

import setuptools

try:
	with open("README.md", "r") as fh:
		long_description = fh.read()
except FileNotFoundError:
	long_description = """
	# Sailboat
	A quick and easy way to distribute your Python projects!
	### Contributors
	- Cole Wilson
	### Contact
	<cole@colewilson.xyz>
	"""

options = {
	"name": "sailboat",
	"version": "0.25.5",
	"scripts": [],
	"entry_points": {'console_scripts': ['sail=sailboat.__main__:main', 'ssail=sailboat.__main__:main', 'sssail=sailboat.__main__:main', 'ssssail=sailboat.__main__:main', 'sailboat=sailboat.__main__:main', 'ssailboat=sailboat.__main__:main', 'sssailboat=sailboat.__main__:main', 'ssssailboat=sailboat.__main__:main'], 'sailboat_plugins': ['quickstart=sailboat.core:QuickStart', 'remove=sailboat.core:Remove', 'add=sailboat.core:Add', 'git=sailboat.core:Git', 'dev=sailboat.core:Develop', 'release=sailboat.core:Release', 'plugins=sailboat.core:ManagePlugins', 'wizard=sailboat.core:Wizard', 'build=sailboat.build:Build', 'pypi=sailboat.builders:PyPi', 'homebrew=sailboat.builders:Homebrew', 'pyinstaller=sailboat.builders:PyInstaller', 'actions=sailboat.builders:Actions', 'tasks=sailboat.other:Tasks', 'build_docs_readme=sailboat.other:BuildDocs', 'setcodeversion=sailboat.other:SetVersion']},
	"author": "Cole Wilson",
	"author_email": "cole@colewilson.xyz",
	"description": "A quick and easy way to distribute your Python projects!",
	"long_description": long_description,
	"long_description_content_type": "text/markdown",
	"url": "https://github.com/cole-wilson/sailboat",
	"packages": setuptools.find_packages(),
	"install_requires": ['toml', 'semver', 'requests', 'setuptools', 'twine', 'colorama', 'enlighten', 'blessed'],
	"classifiers": ["Programming Language :: Python :: 3"],
	"python_requires": '>=3.6',
	"package_data": {"": ['resources/*', 'plugins.json'], },
	"license": "MIT",
	"keywords": 'sail package python setup.py sailboat shipsnake distribute ship snake snek release build',
	"setup_requires": ['wheel'],
}

custom_options = {}

if __name__ == "__main__":
	setuptools.setup(**custom_options, **options)
