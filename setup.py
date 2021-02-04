#!/usr/bin/env python3

# +------------------------+			   
# | Created with Sailboat  |			   
# |			                   |			   
# | Do not edit this file  |			   
# | directly. Instead  	   |			   
# | you should edit the	   |			   
# | `sailboat.toml` file.  |			   
# +------------------------+	

import setuptools

try:
  with open("README.md", "r") as fh:
	  long_description = fh.read()
except:
	long_description = "# Sailboat\nA quick and easy way to distribute your Python projects!\n### Contributors\n- Cole Wilson\n### Contact\n<cole@colewilson.xyz> "

options = {
	"name":"sailboat",
	"version":"0.24.13",
	"scripts":[],
	"entry_points":{'console_scripts': ['sail=sailboat.__main__:main', 'sailboat=sailboat.__main__:main'], 'sailboat_plugins': ['quickstart=sailboat.core:QuickStart', 'pypi=sailboat.builders:PyPi', 'homebrew=sailboat.builders:Homebrew', 'pyinstaller=sailboat.builders:PyInstaller', 'dev=sailboat.core:Develop', 'release=sailboat.core:Release', 'build=sailboat.build:Build', 'wizard=sailboat.core:Wizard', 'remove=sailboat.core:Remove', 'add=sailboat.core:Add', 'plugins=sailboat.core:ManagePlugins', 'git=sailboat.core:Git', 'tasks=sailboat.other:Tasks', 'workflow=sailboat.core:Actions', 'github=sailboat.core:Git', 'github_release=sailboat.core:GithubRelease', 'build_docs_readme=sailboat.other:BuildDocs', 'setcodeversion=sailboat.other:SetVersion']},
	"author":"Cole Wilson",
	"author_email":"cole@colewilson.xyz",
	"description":"A quick and easy way to distribute your Python projects!",
	"long_description":long_description,
	"long_description_content_type":"text/markdown",
	"url":"https://github.com/cole-wilson/sailboat",
	"packages":setuptools.find_packages(),
	"install_requires":['toml', 'semver', 'requests', 'setuptools', 'twine', 'colorama'],
	"classifiers":["Programming Language :: Python :: 3"],
	"python_requires":'>=3.6',
	"package_data":{"": ['resources/*', 'plugins.json', 'autocomplete', 'auto.bash'],},
	"license":"MIT",
	"keywords":'',
}

custom_options = {}

if __name__=="__main__":
	setuptools.setup(**custom_options,**options)