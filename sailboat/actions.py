import sailboat.build
import toml
import sys
import os

with open('sailboat.toml') as file:
	data = toml.loads(file.read())

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