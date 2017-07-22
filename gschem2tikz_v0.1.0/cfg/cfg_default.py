





# gschem2tikz_align {dictionary}
#
# Stores the complete default GUI config
GuiConfig_default = {
	'maintab/general/outputfilenameformatbox/layout' : {'strprefix': '', 'booloriginalname': 'True', 'strsuffix': ''} ,
	'maintab/general/outputfilesavemodebox/layout' : {'boolsaveoriginaldirectory': 'True', 'boolsaveindividualfile': 'False', 'boolsaveallfilessamedirectory': 'False'} ,
	'maintab/general/otherbox/layout' : {'boolletgschemsetattributestoshow': 'False', 'boolincludetikzenvironment': 'True'} ,
	'maintab/libraries/dependanceoptionsbox/layout' : {'listgschemsymbolsdirectories': "['/usr/share/gEDA/sym/']"} ,
	'maintab/thickness/schematiclinewidthbox/layout' : {'floatline': '0.5', 'floatbus': '1.0', 'floatnet': '0.5', 'floatboxline': '0.5', 'floatcircleline': '0.5', 'floatarcline': '0.5', 'floatpinline': '0.5', 'floatpinheadline': '0.2'} ,
	'maintab/thickness/componentlinewidthbox/layout' : {'floatline': '0.5', 'floatbus': '1.0', 'floatnet': '0.5', 'floatboxline': '0.5', 'floatcircleline': '0.5', 'floatarcline': '0.5', 'floatpinline': '0.5', 'floatpinheadline': '0.2'} ,
	'maintab/thickness/textalignmentdistancebox/schematiclayout' : {'floatschematic': '0.2'} ,
	'maintab/thickness/textalignmentdistancebox/componentlayout' : {'floatcomponent': '0.2'} ,
	'maintab/colors/layout' : {'strbackground': 'white', 'strpin': 'black', 'strnetendpoint': 'black', 'strnet': 'black', 'strgraphic': 'black', 'strattribute': 'black', 'strlogicbubble': 'black', 'strgridpoint': 'black', 'strdetachedattribute': 'black', 'strselection': 'black', 'strboundingbox': 'black', 'strzoombox': 'black', 'strtext': 'black', 'strbus': 'black', 'strstroke': 'black', 'strlock': 'black', 'strnetjunction': 'black', 'strmeshgridmayor': 'black', 'strmeshgridminor': 'black'} ,
	'maintab/colordefinitions/layout' : {'colortable': "[['dkred',0.6,0,0],['dkgreen',0,0.6,0,1.0],['dkblue',0,0,0.6]]"} ,
	'maintab/schematicattributes/symbolonly/layout' : {'booldevice': 'False', 'boolgraphical': 'False', 'booldescription': 'False', 'boolcomment': 'False', 'boolpinseq': 'False', 'boolpinnumber': 'False', 'boolpintype': 'False', 'boolpinlabel': 'False', 'boolnumslots': 'False', 'boolslotdef': 'False', 'boolfootprint': 'False', 'booldocumentation': 'False'} ,
	'maintab/schematicattributes/schematiconly/layout' : {'boolnetname': 'False', 'boolsource': 'False'} ,
	'maintab/schematicattributes/symbolandschematic/layout' : {'boolrefdes': 'True', 'boolslot': 'False', 'boolnet': 'False', 'boolvalue': 'False', 'boolsymversion': 'False', 'booldistlicense': 'False', 'booluselicense': 'False'} ,
	'maintab/schematicattributes/other/layout' : {'boolfile': 'False', 'boolauthor': 'False', 'boolpins': 'False'} ,
	'maintab/schematicattributes/modelproperties/layout' : {'boolmodelname': 'False', 'boolmodel': 'False'} ,
	'maintab/componentattributes/symbolonly/layout' : {'booldevice': 'False', 'boolgraphical': 'False', 'booldescription': 'False', 'boolcomment': 'False', 'boolpinseq': 'False', 'boolpinnumber': 'False', 'boolpintype': 'False', 'boolpinlabel': 'False', 'boolnumslots': 'False', 'boolslotdef': 'False', 'boolfootprint': 'False', 'booldocumentation': 'False'} ,
	'maintab/componentattributes/schematiconly/layout' : {'boolnetname': 'False', 'boolsource': 'False'} ,
	'maintab/componentattributes/symbolandschematic/layout' : {'boolrefdes': 'False', 'boolslot': 'False', 'boolnet': 'False', 'boolvalue': 'False', 'boolsymversion': 'False', 'booldistlicense': 'False', 'booluselicense': 'False'} ,
	'maintab/componentattributes/other/layout' : {'boolfile': 'False', 'boolauthor': 'False', 'boolpins': 'False'} ,
	'maintab/componentattributes/modelproperties/layout' : {'boolmodelname': 'False', 'boolmodel': 'False'} ,
}


# gschem2tikz_align {dictionary}
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

# gschem2gschemlabel_colors {dictionary}
#
# Translate the gschem color numeration to gschem color layer

gschem2gschemlayer_colors = {
	'0'				: 'strbackground',
	'1'				: 'strpin',
	'2'				: 'strnetendpoint',
	'3'				: 'strgraphic',
	'4'				: 'strnet',
	'5'				: 'strattribute',
	'6'				: 'strlogicbubble',
	'7'				: 'strgridpoint',
	'8'				: 'strdetachedattribute',
	'9'				: 'strtext',
	'10'			: 'strbus',
	'11'			: 'strselection',
	'12'			: 'strboundingbox',
	'13'			: 'strzoombox',
	'14'			: 'strstroke',
	'15'			: 'strlock',
	'16'			: 'strnetjunction',
	'17'			: 'strmeshgridmajor',
	'18'			: 'strmeshgridminor',
}
