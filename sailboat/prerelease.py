import sys
# Prerelease checker given GitHub tag.
if "dev" in sys.argv[1]:
	print('prerel=true')
elif "beta" in sys.argv[1]:
	print('prerel=true')
elif "alpha" in sys.argv[1]:
	print('prerel=true')
elif "test" in sys.argv[1]:
	print('prerel=true')

else:
	print('prerel=false')