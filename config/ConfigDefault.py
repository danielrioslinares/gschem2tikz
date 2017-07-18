#!/usr/bin/python

from configparser import SafeConfigParser



# gschem2tikz_thickness_main {global dictionary}
#
# Stores the thickness of the different blocks from main layer

gschem2tikz_thickness_main = {
	'line' : 0.8, # Line width (in pts)
	'bus' : 1.6, # Bus line width (in pts)
	'net' : 0.8, # Net line width (in pts)
	'box' : 0.8, # Box line width (in pts)
	'circle' : 0.8, # Circle line width (in pts)
	'arc' : 0.8, # Arc line width (in pts)
	'pinline' : 0.8, # Pin line width (in pts)
	'pinhead' : 0.5, # Pin knot head radius (in pts)
	'inner sep' : 0.5, # Distance between text and anchor (in pts)
}

# gschem2tikz_thickness_child {global dictionary}
#
# Stores the thickness of the different blocks from child layers

gschem2tikz_thickness_child = {
	'line' : 0.8, # Line width (in pts)
	'bus' : 1.6, # Bus line width (in pts)
	'net' : 0.8, # Net line width (in pts)
	'box' : 0.8, # Box line width (in pts)
	'circle' : 0.8, # Circle line width (in pts)
	'arc' : 0.8, # Arc line width (in pts)
	'pinline' : 0.8, # Pin line width (in pts)
	'pinhead' : 0.5, # Pin knot head radius (in pts)
	'inner sep' : 0.5, # Distance between text and anchor (in pts)
}

# gschem2tikz_align {global dictionary}
#
# Translate the gschem numeration of the alignment of text to tikz node argument

gschem2tikz_align = {
	'0'				: 'above right',
	'1'				: 'right',
	'2'				: 'below right',
	'3'				: 'above',
	'4'				: 'centered',
	'5'				: 'below',
	'6'				: 'above left',
	'7'				: 'left',
	'8'				: 'below left',
}

# gschem_attributes_main_shown {global dictionary}
#
# Storages attributes to not be shown in the general schematic

gschem_attributes_main_shown = {
	# Standard attributes
	'netname'		: False,
	'footprint'		: False,
	'value'			: False,
	'refdes'		: True,
	'source'		: False,
	'model-name'	: False,
	'model'			: False,
	'net'			: False,
	'device'		: False,
	'pinnumber'		: True,
	'pinseq'		: False,
	'pintype'		: False,
	'pinlabel'		: False,
	'numslots'		: False,
	'slot'			: False,
	'slotdef'		: False,
	'graphical'		: False,
	'description'	: False,
	'documentation'	: False,
	'symversion'	: False,
	'comment'		: False,
	'author'		: False,
	'dist-license'	: False,
	'use-license'	: False,
	'file'			: False,
	# Other non-standard attributes
	'class'			: False,
	'pins'			: False,
}

# gschem_attributes_child_shown {global dictionary}
#
# Storages attributes to not be shown inside the components

gschem_attributes_child_shown = {
	# Standard attributes
	'netname'		: False,
	'footprint'		: False,
	'value'			: False,
	'refdes'		: False,
	'source'		: False,
	'model-name'	: False,
	'model'			: False,
	'net'			: False,
	'device'		: False,
	'pinnumber'		: False,
	'pinseq'		: False,
	'pintype'		: False,
	'pinlabel'		: False,
	'numslots'		: False,
	'slot'			: False,
	'slotdef'		: False,
	'graphical'		: False,
	'description'	: False,
	'documentation'	: False,
	'symversion'	: False,
	'comment'		: False,
	'author'		: False,
	'dist-license'	: False,
	'use-license'	: False,
	'file'			: False,
	# Other non-standard attributes
	'class'			: False,
	'pins'			: False,
}

# gschem2gschemlabel_colors {global dictionary}
#
# Translate the gschem color numeration to gschem color layer

gschem2gschemlayer_colors = {
	'0'				: 'background',
	'1'				: 'pin',
	'2'				: 'net endpoint',
	'3'				: 'graphic',
	'4'				: 'net',
	'5'				: 'attribute',
	'6'				: 'logic bubble',
	'7'				: 'grid point',
	'8'				: 'detached attribute',
	'9'				: 'text',
	'10'			: 'bus',
	'11'			: 'selection',
	'12'			: 'bounding box',
	'13'			: 'zoom box',
	'14'			: 'stroke',
	'15'			: 'lock',
	'16'			: 'net junction',
	'17'			: 'mesh grid major',
	'18'			: 'mesh grid minor',
}

# gschemlayer2tikz_colors {global dictionary}
# 	keys:
# 		-> gschem palette : clone of the colors that gschem uses
# 		-> tikz palette : recommended colors for tikz
#
# Color palette for the drawn
gschemlayer2tikz_colors = {
	'gschem' : {
		'background'			: 'black',
		'pin'					: 'white',
		'net endpoint'			: 'red',
		'net'					: 'blue',
		'graphic'				: 'green',
		'attribute'				: 'yellow',
		'logic Bubble'			: 'cyan',
		'grid Point'			: 'gray',
		'detached attribute'	: 'red',
		'selection'				: 'orange',
		'bounding box'			: 'orange',
		'zoom box'				: 'cyan',
		'text'					: 'green',
		'bus'					: 'green',
		'stroke'				: 'lightgray',
		'lock'					: 'gray',
		'net junction'			: 'yellow',
		'mesh grid mayor'		: 'black',
		'mesh grid minor'		: 'black',
		},
	'tikz' : {
		'background'			: 'white',
		'pin'					: 'black',
		'net endpoint'			: 'black',
		'net'					: 'blue',
		'graphic'				: 'black',
		'attribute'				: 'black',
		'logic Bubble'			: 'cyan',
		'grid Point'			: 'gray',
		'detached attribute'	: 'black',
		'selection'				: 'orange',
		'bounding box'			: 'orange',
		'zoom box'				: 'cyan',
		'text'					: 'black',
		'bus'					: 'green',
		'stroke'				: 'lightgray',
		'lock'					: 'gray',
		'net junction'			: 'black',
		'mesh grid mayor'		: 'black',
		'mesh grid minor'		: 'black',
		},
}



default_dics = [
	gschem2tikz_thickness_main,
	gschem2tikz_thickness_child,
	gschem2tikz_align,
	gschem_attributes_main_shown,
	gschem_attributes_child_shown,
	gschem2gschemlayer_colors,
	gschemlayer2tikz_colors['tikz']
]

default_lbls = [
	'gschem2tikz_thickness_main',
	'gschem2tikz_thickness_child',
	'gschem2tikz_align',
	'gschem_attributes_main_shown',
	'gschem_attributes_child_shown',
	'gschem2gschemlayer_colors',
	'gschemlayer2tikz_colors',
]

from Config import write_cfg

write_cfg(default_dics,default_lbls,'config_default.ini')





#
