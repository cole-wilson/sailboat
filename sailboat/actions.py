import sailboat.build
import toml
import sys
import os

try:
	data = toml.loads(open('.'+os.sep+'sailboat.toml').read())
except toml.decoder.TomlDecodeError as e:
	print('Config error:\n\t'+str(e))
	exit()

try:
	import wheel
except:
	os.system('pip install wheel')

if sys.platform.startswith('win'):
	sailboat.build.main(data['latest_build'],[],nointeraction=True)


elif sys.platform.startswith('darwin') or True:
	sailboat.build.main(data['latest_build'],[],nointeraction=True)

else:
	print('This is not being run on Mac and Windows.')