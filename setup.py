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
	long_description = "# Sailboat\nA quick and easy way to package, freeze, and distribute your Python projects!\n### Contributors\n- Cole Wilson\n### Contact\n<cole@colewilson.xyz> "

options = {
	"name":"sailboat",
	"version":"0.0.8",
	"scripts":[],
	"entry_points":{
		'console_scripts': ['sail=sailboat.__main__:main', 'sailboat=sailboat.__main__:main'],
	},
	"author":"Cole Wilson",
	"author_email":"cole@colewilson.xyz",
	"description":"A quick and easy way to package, freeze, and distribute your Python projects!",
	"long_description":long_description,
	"long_description_content_type":"text/markdown",
	"url":"https://github.com/cole-wilson/sailboat",
	"packages":setuptools.find_packages(),
	"install_requires":['toml', 'requests'],
	"classifiers":["Programming Language :: Python :: 3"],
	"python_requires":'>=3.6',
	"package_data":{"": ['resources/*', '*.template', '*.template*', '*.txt'],},
	"license":"MIT",
	"keywords":'ship distribute package snake python freeze shipsnake setuptools sailboat',
}

custom_options = {}

if __name__=="__main__":
	setuptools.setup(**custom_options,**options)