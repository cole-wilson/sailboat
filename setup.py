#!/usr/bin/env python3

# +------------------------+                       
# | Created with Sailboat  |                       
# |                        |                       
# | Do not edit this file  |                       
# | directly. Insead       |                       
# | you should edit the    |                       
# | `sailboat.toml` file.  |                       
# +------------------------+    

import setuptools

try:
  with open("README.md", "r") as fh:
      long_description = fh.read()
except:
	long_description = "# Sailboat\nA quick and easy way to distribute your python projects!\n### Contributors\n- Cole Wilson\n### Contact\n<cole@colewilson.xyz> "

setuptools.setup(
    name="sailboat",
    version="0.0.3dev2",
		scripts=['bin/sailboat'],
#		entry_points={
#			'console_scripts': ['sailboat=sailboat.__main__.main()'],
#		},
    author="Cole Wilson",
    author_email="cole@colewilson.xyz",
    description="A quick and easy way to distribute your python projects!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cole-wilson/sailboat",
    packages=setuptools.find_packages(),
		install_requires=['toml'],
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
		package_data={"": ['*.template', '*.template.*', 'txt'],},
		license="MIT",
		keywords='ship distribute package snake python freeze shipsnake setuptools sailboat',
)