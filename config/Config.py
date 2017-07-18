#!/usr/bin/python

from configparser import SafeConfigParser

""" Write/read settings file methods """

# write_cfg(dics,lbls,file) {void function(list<dic> dics, list<str> lbls, str file)}
#	@param dics : contains all configuration dictionaries to save
#	@param lbls : contains all configuration dictionaries labels to save
#	@param file : name of the settings file (extension must be included)
#
# Generates a settings file (.ini)
# 	@example : write_cfg(dics,lbls,'settings.ini')
def write_cfg(dics,lbls,file):

	cfg = SafeConfigParser()

	for dic,lbl in zip(dics,lbls):
		cfg.add_section(lbl)
		for k in dic:
			cfg.set(lbl, k, str(dic[k]))

	with open(file,'w') as f: cfg.write(f)

# read_cfg(file) {void function(list<dic> dics, list<str> lbls)}
#	@param file : name of the settings file (extension must be included)
#
# Read a settings file (.ini)
# 	@example : dics,lbls = read_cfg('settings.ini')
def read_cfg(file):
	cfg = SafeConfigParser()
	cfg.readfp(open(file))

	dics = []
	lbls = []
	for section in cfg.sections():
		dictionary = {}
		for k in cfg.options(section):
			dictionary[k] = cfg.get(section, k)
		dics.append(dictionary)
		lbls.append(section)

	return dics,lbls

# read_cfg(file) {void function(list<dic> dics, list<str> lbls)}
#	@param file : name of the settings file (extension must be included)
#
# Read a settings file (.ini)
# 	@example : dics,lbls = read_cfg('settings.ini')
def read_cfg(file,section,key):
	cfg = SafeConfigParser()
	cfg.readfp(open(file))
	return cfg.get(section, key)

#
