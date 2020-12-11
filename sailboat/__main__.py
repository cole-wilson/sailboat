# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

def main():
	import sys
	import getopt
	import os

	he = "Provide a mode:\n\t"+sys.argv[0].split('/')[-1]+" [wizard | build | dev | git | release]"

	try:
		arguments, ids = getopt.getopt(sys.argv[1:], "fyn", ['pypi-only','pyinstaller-only','homebrew-only','actions-only','windows-only','mac-only'])
	except:
		print(he)
		sys.exit(0)

	noint = ('-y','') in arguments

	try:
		mode = ids[0]
	except:
		print(he)
		sys.exit(0)

	try:
		version = ids[1]
	except:
		version = ''

	if version=='' and mode in ["build"]:
		print("Provide a version:\n\t"+sys.argv[0].split('/')[-1]+" "+mode+" <version>")
		sys.exit(0)

	if mode=="dev" and version=="":
		version = "dev_build"

	# ================================================================

	if mode == "wizard":
		import sailboat.wizard as wizard
		wizard.main()

	elif mode == "build":
		import sailboat.build as build
		build.main(version,arguments,nointeraction=noint)

	elif mode == "release":
		import sailboat.release as release
		release.main(arguments,ids)
	# elif mode in ["build","dev","release"]:

	elif mode == "dev":
		os.system('python3 ./setup.py develop')

	elif mode == "git":
		import sailboat.git as git
		git.main()
	else:
		print('Invalid option')
		print(he)

	# 	elif mode == "dev":
	# 		os.system('python3 .'+os.sep+'setup.py develop')
	# 	for x in glob.glob('*.egg-info'):
	# 		shutil.rmtree(x)
	# else:
	# 	print(f'Illegeal option `{mode}`')
	# 	sys.exit(0)

	# if mode=="release":
	# 	print("Please make sure that you have a https://pypi.org/ account.")
	# 	try:
	# 		import twine
	# 	except:
	# 		input('Press enter to continue installing `twine`. Press ctrl+x to exit.')
# 		os.system('python3 -m pip install --user --upgrade twine || python3 -m pip install --upgrade twine')
# 	os.system('python3 -m twine release dist'+os.sep+'*')
if __name__=='__main__':
	main()