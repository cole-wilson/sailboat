# This is just to make markdown docs pages, you should ignore it.
import sys
import json

a = ""

plugs = json.loads(open('sailboat/plugins.json').read())['core']
while True:
	try:
		a += input()+"\n"
	except EOFError:
		break

print('''---
name: {name}
---

# {name}

{desc}

```bash
'''.format(name=sys.argv[1],desc=plugs[sys.argv[1]]['description'].capitalize()))
print(a)
print('''```''')