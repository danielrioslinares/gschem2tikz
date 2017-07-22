

from core.TikZ import *
import os

# Schematic {class(file,preset,directories)}
# 	@param file : file that contains the gschem schematic
# 	@param preset : config file that contains the settings
# 	@param directories : directories to find all components in the schematic
#
# Creates a schematic with all information about it
class Schematic:

	def __init__(self, file, preset, directories, gc):
		self.file = file
		self.gc = gc
		self.directories = directories
		self.tikz_shapes = self.dic2shapes(*self.generate_shapes())

	# find_component(component) {str path function(str component)}
	# 	@param component : component name to find
	#
	# Used to locate a component in the libraries
	# 	@example : Schematic.find_component('resistor-1.sym')
	def find_component(self, component):
		for d in self.directories:
			for f in os.walk(d):
				for g in f[2]:
					if g == component or g == component.replace('.sym','.tikz'):
						if f[0][-1] != '/':
							return f[0] +'/' + g
						else:
							return f[0] + g
						break
		return 'missing.sym'

	# generate_shapes(file,child_layer) {list<Shapes> function(str file, bool child_layer)}
	# 	@param file : file to analyze from gschem
	# 	@param child_layer : if True, then apply the gc child properties
	#
	# Creates a list of Shapes from a class (TikZ class)
	# 	@example : Schematic.generate_shapes()
	def generate_shapes(self, file = None, child_layer = False):

		gc = self.gc
		if file == None: file = self.file

		with open(file, 'r') as myfile:
			# Read and split the data to list of lines
		    temp = myfile.read().split('\n')

		# Split floato fields
		temp = [line.split() for line in temp]

		# Let's filter the information of the file
		ignore_list = ['v', None, '{', '}']

		data = []
		for line in temp:
			# First of all remove all empty lines
			if len(line) != 0:
				# From ignore_list filter all useless lines
				ignore_line = False
				for ignore_char in ignore_list:
					if line[0] == ignore_char: ignore_line = True
				if ignore_line == False:
					data.append(line)

		# For pictures and text, the next line is the path to the image or the text
		lines_to_remove = []
		for i in range(len(data)):
			# 'G' is picture and 'T' is text
			if data[i][0] == 'G' or data[i][0] == 'T':
				data[i] += data[i+1]
				lines_to_remove.append(i+1)

		for i in reversed(lines_to_remove): del(data[i])

		# Now it's time to create a list of dictionaries for each type of block

		scale = 0.001

		texts = []
		lines = []
		buses = []
		netss = []
		boxes = []
		picts = []
		arcss = []
		comps = []
		tikz_comps = []
		circs = []
		pinss = []

		for line in data:
			try:
				# Line
				if line[0] == 'L':
					dic = {
						'type' : 'line',
						'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
						'color' : gc.get_colorFromGschem(line[5]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatline','str'),
					}
					lines.append(dic)
				# Net
				if line[0] == 'N':
					dic = {
						'type' : 'net',
						'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
						'color' : gc.get_colorFromGschem(line[5]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatnet','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatnet','str'),
					}
					netss.append(dic)
				# Bus
				if line[0] == 'U':
					dic = {
						'type' : 'bus',
						'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
						'color' : gc.get_colorFromGschem(line[5]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatbus','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatbus','str'),
					}
					buses.append(dic)
				# Box (rectangle)
				if line[0] == 'B':
					dic = {
						'type' : 'box',
						'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'XY2' : [format((float(line[1])+float(line[3]))*scale,'.6f'),format((float(line[2])+float(line[4]))*scale,'.6f')],
						'color' : gc.get_colorFromGschem(line[5]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatboxline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatboxline','str'),
						'fillcolor' : None,
					}
					boxes.append(dic)
				# Circles
				if line[0] == 'V':
					dic = {
						'type' : 'circle',
						'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'radius' : format(float(line[3])*scale,'.6f'),
						'color' : gc.get_colorFromGschem(line[4]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatcircleline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatcircleline','str'),
						'fillcolor' : None,
					}
					circs.append(dic)
				# Arcs
				if line[0] == 'A':
					dic = {
						'type' : 'arc',
						'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'radius' : format(float(line[3])*scale,'.6f'),
						'start_angle' : format(float(line[4]),'.6f'),
						'sweep_angle' : format(float(line[5]),'.6f'),
						'color' : gc.get_colorFromGschem(line[6]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatarcline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatarcline','str'),
						'fillcolor' : None,
					}
					arcss.append(dic)
				# Pictures
				if line[0] == 'G':
					dic = {
						'type' : 'picture',
						'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'alignment' : 'centered',
						'text' : '\\includegraphics[width = ' + str(float(line[3])*scale) + ']{' + line[8] + '}'
					}
					picts.append(dic)
				# Text boxes
				if line[0] == 'T':
					attr = 'bool'+line[10].split('=')[0]
					# Hide certain attributes inside components
					try:
						if child_layer:
							for sec in ['maintab/componentattributes/symbolonly/layout','maintab/componentattributes/schematiconly/layout','maintab/componentattributes/symbolandschematic/layout','maintab/componentattributes/other/layout','maintab/componentattributes/modelproperties/layout']:
								try:
									shown = gc.get_cfg(sec,attr,'bool')
									line[10] = line[10].split('=')[1]
								except: shown = shown
						# Hide certain attributes outside components
						else:
							for sec in ['maintab/schematicattributes/symbolonly/layout','maintab/schematicattributes/schematiconly/layout','maintab/schematicattributes/symbolandschematic/layout','maintab/schematicattributes/other/layout','maintab/schematicattributes/modelproperties/layout']:
								try:
									shown = gc.get_cfg(sec,attr,'bool')
									line[10] = line[10].split('=')[1]

								except: shown = shown
					except:
						shown = True
					if gc.get_cfg('maintab/general/otherbox/layout','boolletgschemsetattributestoshow','bool') and not child_layer:
						shown = True if line[5] == '0' else False
					# Text box if shown
					if shown:
						text = ' '.join([line[i] for i in range(10,len(line))])
						dic = {
							'type' : 'text',
							'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
							'color' : gc.get_colorFromGschem(line[3]),
							'rotate' : line[7],
							'size' : line[4],
							'text' : text,
							'inner sep' : gc.get_cfg('maintab/thickness/textalignmentdistancebox/componentlayout','floatcomponent','str') if child_layer else gc.get_cfg('maintab/thickness/textalignmentdistancebox/schematiclayout','floatschematic','str'),
							'alignment' : gc.get_alignFromGschem(line[8]),
						}
						texts.append(dic)
				# Pin
				if line[0] == 'P':
					if int(line[7]) == 0:
						XY1 = [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')]
						XY2 = [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')]
					else:
						XY2 = [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')]
						XY1 = [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')]
					dic = {
						'type' : 'pin',
						'XY1' : XY1,
						'XY2' : XY2,
						'color' : gc.get_colorFromGschem(line[5]),
						'headcolor' : gc.get_colorFromGschem(line[5]),
						'thickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinline','str'),
						'headthickness' : gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinheadline','str') if child_layer else gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinheadline','str'),
					}
					pinss.append(dic)
				# Component
				if line[0] == 'C':
					component = self.find_component(line[6])
					if component[-1] == 'z':
						with open(component,'r') as f:
							tikz_scope = f.read()
						dic = {
							'type' : 'tikzcomponent',
							'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
							'mirror' : True if line[5] == '1' else False,
							'rotate' : line[4],
							'component' : line[6],
							'tikz_scope' : tikz_scope,
						}
						tikz_comps.append(dic)
					elif component[-1] == 'm':
						dic = {
							'type' : 'component',
							'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
							'mirror' : True if line[5] == '1' else False,
							'rotate' : line[4],
							'component' : line[6],
							'tikz_shapes' : self.dic2shapes(*self.generate_shapes(component, True)),
						}
						comps.append(dic)
			except:
				pass
		return texts, lines, buses, netss, boxes, picts, arcss, comps, tikz_comps, circs, pinss


	def dic2shapes(self, texts, lines, buses, netss, boxes, picts, arcss, comps, tikz_comps, circs, pinss):
		tikz_shapes = []
		line_list = []
		for line in lines:
			line_list.append( Line(line['XY1'], line['XY2'], line['color'], line['thickness']) )

		if len(lines) > 1:
			plines = PolyLines( line_list, color = lines[0]['color'], thickness = lines[0]['thickness'] )
			for line in plines.line_list:
				tikz_shapes.append(line)
		else:
			for line in lines:
				tikz_shapes.append( Line(line['XY1'], line['XY2'], line['color'], line['thickness']) )

		for box in boxes:
			tikz_shapes.append( Box(box['XY1'], box['XY2'], box['color'], box['thickness'], box['fillcolor']) )

		for circle in circs:
			tikz_shapes.append( Circle(circle['XY'], circle['radius'], circle['color'], circle['thickness']) )

		for arc in arcss:
			tikz_shapes.append( Arc(arc['XY'], arc['radius'], arc['start_angle'], arc['sweep_angle'], arc['color'], arc['thickness'], arc['fillcolor']) )

		for text in texts:
			tikz_shapes.append( Node(text['XY'], text['text'], text['size'], text['rotate'], text['alignment'], text['color'], text['inner sep']) )

		for pin in pinss:
			tikz_shapes.append( Pin(pin['XY1'], pin['XY2'], pin['color'], pin['headcolor'], pin['thickness'], pin['headthickness']) )

		for comp in comps:
			tikz_shapes.append( Component(comp['XY'], comp['tikz_shapes'], comp['rotate'], comp['mirror']) )

		for tikz_comp in tikz_comps:
			tikz_shapes.append( TikZComponent(tikz_comp['XY'], tikz_comp['tikz_scope'], tikz_comp['rotate'], tikz_comp['mirror']) )

		self.tikz_shapes = tikz_shapes
		return tikz_shapes

	def draw(self):
		draw = ''
		for shape in self.tikz_shapes:
			draw += shape.draw()
		return draw


	def get_file(self): return self.file
