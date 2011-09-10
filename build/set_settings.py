import ConfigParser, os, sys

config = ConfigParser.ConfigParser()
config.read(['buildout.cfg'])
config.set('django', 'settings', sys.argv[1])
with open('buildout.cfg', 'wb') as of:
	config.write(of)



