import glob
import os

licensetext = """# Copyright 2020 Cole Wilson and other contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""

def pre(version,data):
	# Add License Header
	if 'extras' not in data:
		data['extras'] = {}
	if 'licensed_files' not in data['extras']:
		data['extras']['licensed_files'] = []
	for x in glob.glob(os.path.join('sailboat','*.py')):
		if x not in data['extras']['licensed_files']:
			data['extras']['licensed_files'].append(x)
			try:
				f = open(x,'r')
				temp = f.read()
				f.close()
				f = open(x,'w+')
				f.write(licensetext+temp)
				f.close()
				print('Added license header to '+x)
			except:
				print('Error writing license header to '+x)
	return data