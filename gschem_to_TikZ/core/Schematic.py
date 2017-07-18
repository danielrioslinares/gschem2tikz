

from config.Parser_gschem2tikz import Parser_gschem2tikz
from core.TikZ import *
import os

# Schematic {class(file,preset,directories)}
# 	@param file : file that contains the gschem schematic
# 	@param preset : config file that contains the settings
# 	@param directories : directories to find all components in the schematic
#
# Creates a schematic with all information about it
class Schematic:

	def __init__(self, file, preset, directories):
		self.file = file
		self.g2t = Parser_gschem2tikz(preset)
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
					if g == component:
						if f[0][-1] != '/':
							return f[0] +'/' + g
						else:
							return f[0] + g
						break
		return 'missing.sym'

	# generate_shapes(file,g2t,child_layer) {list<Shapes> function(str file, Parser_gschem2tikz g2t, bool child_layer)}
	# 	@param file : file to analyze from gschem
	# 	@param g2t : Parser_gschem2tikz object that returns all properties required
	# 	@param child_layer : if True, then apply the g2t child properties
	#
	# Creates a list of Shapes from a class (TikZ class)
	# 	@example : Schematic.generate_shapes()
	def generate_shapes(self, file = None, child_layer = False):

		g2t = self.g2t
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
		circs = []
		pinss = []

		for line in data:
			# Line
			if line[0] == 'L':
				dic = {
					'type' : 'line',
					'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
					'color' : g2t.get_color(line[5]),
					'thickness' : str(g2t.get_thickness_child('line')) if child_layer else str(g2t.get_thickness_main('line')),
				}
				lines.append(dic)
			# Net
			if line[0] == 'N':
				dic = {
					'type' : 'net',
					'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
					'color' : g2t.get_color(line[5]),
					'thickness' : str(g2t.get_thickness_child('net')) if child_layer else str(g2t.get_thickness_main('net')),
				}
				netss.append(dic)
			# Bus
			if line[0] == 'U':
				dic = {
					'type' : 'bus',
					'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'XY2' : [format((float(line[3]))*scale,'.6f'),format((float(line[4]))*scale,'.6f')],
					'color' : g2t.get_color(line[5]),
					'thickness' : g2t.get_thickness_child('bus') if child_layer else g2t.get_thickness_main('bus'),
				}
				buses.append(dic)
			# Box (rectangle)
			if line[0] == 'B':
				dic = {
					'type' : 'box',
					'XY1' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'XY2' : [format((float(line[1])+float(line[3]))*scale,'.6f'),format((float(line[2])+float(line[4]))*scale,'.6f')],
					'color' : g2t.get_color(line[5]),
					'thickness' : g2t.get_thickness_child('box') if child_layer else g2t.get_thickness_main('box'),
					'fillcolor' : None,
				}
				boxes.append(dic)
			# Circles
			if line[0] == 'V':
				dic = {
					'type' : 'circle',
					'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'radius' : format(float(line[3])*scale,'.6f'),
					'color' : g2t.get_color(line[4]),
					'thickness' : g2t.get_thickness_child('circle') if child_layer else g2t.get_thickness_main('circle'),
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
					'color' : g2t.get_color(line[6]),
					'thickness' : g2t.get_thickness_child('arc') if child_layer else g2t.get_thickness_main('arc'),
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
				attr = line[10].split('=')[0]
				# Hide certain attributes inside components
				try:
					if child_layer:
						shown = g2t.get_attribute_child_shown(attr)
						line[10] = line[10].split('=')[1]
					# Hide certain attributes outside components
					else:
						shown = g2t.get_attribute_main_shown(attr)
						line[10] = line[10].split('=')[1]
				except:
					shown = True
				# Text box if shown
				if shown:
					text = ' '.join([line[i] for i in range(10,len(line))])
					dic = {
						'type' : 'text',
						'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
						'color' : g2t.get_color(line[3]),
						'rotate' : line[7],
						'size' : line[4],
						'text' : text,
						'inner sep' : g2t.get_thickness_child('inner sep') if child_layer else g2t.get_thickness_main('inner sep'),
						'alignment' : g2t.get_alignment(line[8]),
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
					'color' : g2t.get_color(line[5]),
					'headcolor' : g2t.get_color(line[5]),
					'thickness' : g2t.get_thickness_child('pinline') if child_layer else g2t.get_thickness_main('pinline'),
					'headthickness' : g2t.get_thickness_child('pinhead') if child_layer else g2t.get_thickness_main('pinhead'),
				}
				pinss.append(dic)
			# Component
			if line[0] == 'C':
				dic = {
					'type' : 'component',
					'XY' : [format((float(line[1]))*scale,'.6f'),format((float(line[2]))*scale,'.6f')],
					'mirror' : True if line[5] == '1' else False,
					'rotate' : line[4],
					'component' : line[6],
					'tikz_shapes' : self.dic2shapes(*self.generate_shapes(self.find_component(line[6]), True)),
				}
				comps.append(dic)

		return texts, lines, buses, netss, boxes, picts, arcss, comps, circs, pinss


	def dic2shapes(self,texts, lines, buses, netss, boxes, picts, arcss, comps, circs, pinss):
		tikz_shapes = []
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

		self.tikz_shapes = tikz_shapes
		return tikz_shapes

	def draw(self):
		draw = ''
		for shape in self.tikz_shapes:
			draw += shape.draw()
		return draw
