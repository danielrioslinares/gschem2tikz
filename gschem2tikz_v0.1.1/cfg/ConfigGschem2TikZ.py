
from config.Config import read_cfg


# Parser_gschem2tikz {class(preset)}
# 	@param preset : config file that contains the settings
#
# Translate the gschem numeration and identify the values from the preset
class ConfigGschem2TikZ:

	def __init__(self, preset):
		self.preset = preset

	""" Color methods """

	# get_color(i) {str function(int i)}
	# 	@param i : gschem numeration color code (0 = background, 1 = pin...)
	#
	# Returns the color for the selected preset
	# 	@example : Parser_gschem2tikz.get_color(0)
	def get_color(self,i):
		key = read_cfg(self.preset, 'gschem2gschemlayer_colors', str(i))
		return read_cfg(self.preset, 'gschemlayer2tikz_colors', key)

	# get_alignment(i) {str function(int i)}
	# 	@param i : gschem numeration alignment code (1 = right, 3 = above...)
	#
	# Returns the alignment
	# 	@example : Parser_gschem2tikz.get_alignment(0)
	def get_alignment(self,i):
		return read_cfg(self.preset, 'gschem2tikz_align', str(i))

	# get_attribute_main_shown(key) {str function(str key)}
	# 	@param key : gschem attribute key
	#
	# Returns False when attribute is not shown (main layer)
	# 	@example : Parser_gschem2tikz.get_attribute_main_shown('refdes')
	def get_attribute_main_shown(self,key):
		cond = read_cfg(self.preset, 'gschem_attributes_main_shown', str(key))
		return True if cond == 'True' else False

	# get_attribute_child_shown(key) {str function(str key)}
	# 	@param key : gschem attribute key
	#
	# Returns False when attribute is not shown (child layer)
	# 	@example : Parser_gschem2tikz.get_attribute_child_shown('refdes')
	def get_attribute_child_shown(self,key):
		cond = read_cfg(self.preset, 'gschem_attributes_child_shown', str(key))
		return True if cond == 'True' else False

	# get_thickness_main(key) {str function(str key)}
	# 	@param key : gschem thickness key (line, pinhead, inner sep...)
	#
	# Returns the value in pt of the thickness from main layer
	# 	@example : Parser_gschem2tikz.get_thickness_main('line')
	def get_thickness_main(self,key):
		return read_cfg(self.preset, 'gschem2tikz_thickness_main', str(key))

	# get_thickness_child(key) {str function(str key)}
	# 	@param key : gschem thickness key (line, pinhead, inner sep...)
	#
	# Returns the value in pt of the thickness from main layer
	# 	@example : Parser_gschem2tikz.get_thickness_child('line')
	def get_thickness_child(self,key):
		return read_cfg(self.preset, 'gschem2tikz_thickness_child', str(key))






#
