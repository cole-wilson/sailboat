import os
import glob
import sys


class Plugin:
	"""
	The basic sailboat Plugin class
	"""
	name = ""
	data = {}
	description = "<no description provided>"
	version = ""
	options = []
	setup = {}
	_type = "build"
	_show = True
	_release = False
	_order = 0
	_os = 'linux'
	autocompletion = {}

	def registerAutocompletion(self):
		import __main__
		prefix = self.prefix
		f = open(prefix+"autocomplete",'a')
		for x in self.autocompletion.keys():
			f.write(x+"::"+self.autocompletion[x]+"\n")
	def release(self):
		pass
	def init(self):
		pass
	def add(self):
		self.registerAutocompletion()
		print('Installing...')
	def log(self,message):
		print('\u001b[37m[LOG]: '+message+'\u001b[0m')
	def warn(self,message):
		print('\u001b[33m[WARNING]: '+message+'\u001b[0m')
	def error(self,message):
		print('\u001b[31m[LOG]: '+message+'\u001b[0m')
	def __repr__(self):
		return "<sailboat plugin: "+self.name+">"
	def __init__(self,data=None,options=None,prefix=__file__,name=None,version=None):
		if options!=None:
			self.options = options
		if version!=None:
			self.version = version
		if data!=None:
			self.data = data
		self.name = name	
		self.prefix=prefix
		self.init()
	def storeData(self,key,value):
		if self._type == "core":
			self.data[key] = value
		else:
			if self.name not in self.data[self._type]:
				self.data[self._type][self.name] = {}
			self.data[self._type][self.name][key] = value
	def red(self,string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\u001b[31m"+str(string)+"\033[0m"
	def blue(self,string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\u001b[34m"+str(string)+"\033[0m"
	def section(self,string):
		if sys.platform.startswith('win'):
			return string
		else:
			return "\n\u001b[4m\u001b[1;36m"+str(string)+"\u001b[0m"
	@property
	def data2(self):
		return self.data[self._type][self.name] 
	def getData(self,key=None):
		try:
			if key==None:
				return self.data[self._type][self.name]
			return self.data[self._type][self.name][key]
		except BaseException as e:
			print('Error in {}:\n\t{}'.format(self.name,e))
			return None
	def getResource(self,name,rwmode='r'):
		prefix = os.path.dirname(os.path.abspath(__file__))+os.sep
		return open(prefix+name,rwmode)
	def wizard(self,setup_dict=None):
		if setup_dict == None:
			setup_dict = self.setup
		for key in setup_dict.keys():
			try:
				t = "::".join(key.split('::')[1:])
				key = key.split('::')[0]
			except:
				t = 'str'
			if self._type!="core" and self.name in self.data[self._type] and key in self.data[self._type][self.name]:
				print(self.blue(setup_dict[str(key)+"::"+t])+" "+str(self.data[self._type][self.name][key]))
			elif self._type=="core" and key in self.data:
				print(self.blue(setup_dict[key+"::"+t])+self.data[key])
			elif t=="str":
				self.storeData(key,input("\u001b[34m"+setup_dict[key+"::"+t]+" \u001b[0m"))
			elif t=="int":
				while True:
					try:
						self.storeData(key,int(input("\u001b[34m"+setup_dict[key+"::"+t]+" \u001b[0m")))
						break
					except ValueError:
						print('Please provide an integer.')
			elif t=="bool":
				try:
					self.storeData(key,input("\u001b[34m"+setup_dict[key+"::"+t]+" [y/n] \u001b[0m")[0]=='y')
				except:
					print('error: you did not supply a value!')
					self.storeData(key,input("\u001b[34m"+setup_dict[key+"::"+t]+" [y/n] \u001b[0m")[0]=='y')
			else:
				self.storeData(key,input("\u001b[34m"+setup_dict[key+"::"+t]+" \u001b[0m"))
		return self.data
	def getFiles(self,extension,recursive=True):
		if recursive:
			files = []
			for root,dirs,files in os.walk('.'):
				for filename in files:
					if filename.endswith(extension):
						files.append(root+filename)
			return files
		else:
			return list(glob.glob(extension))
	def run(self,**kwargs):
		print('This plugin has not been set up correctly.\nIf you are the developer, please add a run(self,**kwargs) function to your class.')
		return
