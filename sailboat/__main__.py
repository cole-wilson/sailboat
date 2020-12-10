
def main():
	import sys
	import getopt
	import os

	he = "Provide a mode:\n\tsailboat [wizard | build | dev | release]"

	try:
		arguments, ids = getopt.getopt(sys.argv[1:], "yn", ['pypi-only','pyinstaller-only','homebrew-only','actions-only','windows-only','mac-only'])
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
		print("Provide a version:\n\tsailboat "+mode+" <version>")
		sys.exit(0)

	if mode=="dev" and version=="":
		version = "dev_build"

	# ================================================================

	if mode == "wizard":
		import sailboat.wizard as wizard
		wizard.main()

	elif mode == "build":
		print('This command will build the following:')
		import sailboat.build as build
		build.main(version,arguments,nointeraction=noint)

	elif mode == "release":
		import sailboat.release as release
		release.main(arguments,ids)
	# elif mode in ["build","dev","release"]:

	elif mode == "dev":
		os.system('python3 ./setup.py develop')


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