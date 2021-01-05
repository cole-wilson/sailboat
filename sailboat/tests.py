from sailboat.plugins import Plugin

class Test(Plugin):
	_type="build"
	_release=True
	
	def run(self):
		print('RUN PART')
	
	def release(self):
		print('RELEASE PART')