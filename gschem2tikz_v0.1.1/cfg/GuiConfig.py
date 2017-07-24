#!/usr/bin/python



from configparser import SafeConfigParser
from cfg.cfg_default import *
import os



class GuiConfig:

	''' Write/read settings file methods '''

	# __init__() {void constructor(void)}
	#	@param self.presets_directory {str} : directory where all presets are stored
	#	@param self.cfg_dictionary {dic} : dictionary with all GUI configuration
	#	@param self.preset {str} : directory where is the current preset
	#
	# Generates a settings file (.ini)
	def __init__(self, presets_directory = None, preset = None):
		# Hidden settings folder (~/.gschem2tikz)
		if presets_directory != None: self.presets_directory = presets_directory
		else: self.presets_directory = self.get_settings_directory()

		# Obtain default preset dictionary
		self.cfg_dictionary = GuiConfig_default

		# Now the default template always will be created
		self.write_cfg( self.presets_directory + '/default.ini' )

		# And the default preset is setted
		if preset != None: self.preset = preset
		else: self.preset = self.presets_directory + '/default.ini'

	''' Write/read settings file methods '''

	# write_cfg(f) {void function(dic d, str f)}
	#	@param f : name of the settings file (extension must be included)
	#
	# Generates a settings file (.ini)
	def write_cfg(self, f):

		d = self.cfg_dictionary
		cfg = SafeConfigParser()
		cfg.optionxform = str
		for sec in d:
			cfg.add_section( sec )
			for k in d[sec]:
				cfg.set( sec, k, d[sec][k] )
		try:
			with open(f,'w') as f: cfg.write(f)
			return True
		except:
			return False

	# read_cfg(f) {void function(str f)}
	#	@param f : name of the settings file (extension must be included)
	#
	# Read a settings file (.ini) and stores it in d
	# 	@example : d = read_cfg(os.getenv('HOME') + '/.gschem2tikz/default.ini')
	def read_cfg(self, f):

		cfg = SafeConfigParser()
		cfg.optionxform = str
		cfg.readfp( open(f) )

		sections = [section for section in cfg.sections()]
		d = {}
		for sec in sections:
			d[sec] = {}
			l = {}
			for k in cfg.options( sec ):
				l[k] = cfg.get( sec , k )
				d[sec][k] = l[k]
		return d

	''' Setters '''
	# set_preset() {void function(str p)}
	# 	@param p : preset absolute path
	#
	# Set the preset configuration file
	# 	@example : Object<GuiConfig>.set_preset(preset)
	def set_preset(self, p):
		self.preset = p
		self.cfg_dictionary = self.read_cfg( p )

	# set_cfg(s,k,t) {list<str> function(str s, str k, str t)}
	#	@param s : section of the config dictionary
	#	@param k : key of the section s
	#	@param v : value to set
	#
	# Sets the value @v of a key @k from section @s
	def set_cfg(self,s,k,v):
		self.cfg_dictionary[s][k] = str(v)

	''' Getters '''
	# get_presetsFilenames() {list<str> function(void)}
	#
	# Obtains the filenames of all the presets
	# 	@example : presets = Object<GuiConfig>.get_presetsFilenames()
	def get_presetsFilenames(self):
		return [f for f in os.listdir(self.presets_directory) if f.endswith('.ini')]

	# get_presetsAbsolutePath() {list<str> function(void)}
	#
	# Obtains the filenames of all the presets with the absolute path
	# 	@example : presets = Object<GuiConfig>.get_presetsAbsolutePath()
	def get_presetsAbsolutePath(self):
		return [self.presets_directory + '/' + f for f in self.get_presets()]

	# get_settings_directory() {str function(void)}
	#
	# Obtains the default hidden Linux directory (if doesn't exists, will create it)
	# 	@example : dir = get_settings_directory()
	def get_settings_directory(self):
		directory = os.getenv('HOME') + '/.gschem2tikz'
		if not os.path.exists(directory): os.makedirs(directory)
		return directory

	# get_cfg(s,k,t) {list<str> function(str s, str k, str t)}
	#	@param s : section of the config dictionary
	#	@param k : key of the section s
	#	@param t : return type of the option ('str','bool','list','float')
	#
	# Returns the configuration key
	def get_cfg(self,s,k,t = None):
		c = self.cfg_dictionary[s][k]
		if t == 'bool':
			for b in ['True','true','1','Yes','yes']:
				if c == b: return True
			else: return False
		elif t == 'float':
			return float(c)
		elif t == 'list':
			temp = c.split('[')
			for i in reversed([i for i in range(len(temp)) if temp[i] == '']): del(temp[i])
			for i in range(len(temp)): temp[i] = temp[i].replace('],','').replace(']','').replace("'",'')
			for i in range(len(temp)): temp[i] = temp[i].split(',')
			try:
				for l in temp:
					for j in range(len(l)):
						if l[j][0] == ' ': l[j] = l[j][1:]
				return temp
			except: pass
		else: return c

	''' Getters : gschem immutable configuration '''
	# get_colorFromGschem(i) {str function(int i)}
	#	@param i : gschem color numeration
	#
	# Returns the color from gschem numeration to tikz
	def get_colorFromGschem(self,i):
		key = gschem2gschemlayer_colors[str(i)]
		col = self.get_cfg('maintab/colors/layout',key)
		return col

	# get_alignFromGschem(i) {str function(int i)}
	#	@param i : gschem align numeration
	#
	# Returns the alignment from gschem numeration to tikz
	def get_alignFromGschem(self,i):
		ali = gschem2tikz_align[str(i)]
		return ali

# EOF
