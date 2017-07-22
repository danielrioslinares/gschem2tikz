#!/usr/bin/python



class Line:

	def __init__(self, XY1, XY2, color = None, thickness = None):
		self.XY1 = XY1
		self.XY2 = XY2
		self.color = color
		self.thickness = thickness

	def draw(self):
		draw = '\\draw'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.thickness != None:
			draw += ' [line width = ' + str(self.thickness) + 'pt]'
		coor = '(' + str(self.XY1[0]) + ',' + str(self.XY1[1]) +')--(' + str(self.XY2[0]) + ',' + str(self.XY2[1]) + ')'
		return draw + ' ' + coor + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY1, rotate, mirror)
		x2,y2 = rotate_and_mirror_XY(self.XY2, rotate, mirror)
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]

	def displace(self,XY):
		x1,y1 = float(self.XY1[0])+float(XY[0]),float(self.XY1[1])+float(XY[1])
		x2,y2 = float(self.XY2[0])+float(XY[0]),float(self.XY2[1])+float(XY[1])
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]





class PolyLines:

	def __init__(self, line_list, color = None, thickness = None):
		self.line_list = line_list
		self.XY_list = []
		self.XY1_list = []
		self.XY2_list = []
		self.color = color
		self.thickness = thickness
		self.enroute()

	def compare(self):
		# A string shortcut for coding
		lpl = self.line_list
		# We create a list that will display all dependances
		for i in range(len(lpl)):
			for j in range(len(lpl)):
				# If is ths same line don't make dependance
				if i == j: break
				# comparing list saves the indexes and the nodes with dependance
				comparing = []
				# First of all, find out if i and j share a node:
				if lpl[i].XY1 == lpl[j].XY1: comparing = [i,j,'XY1','XY1']
				if lpl[i].XY1 == lpl[j].XY2: comparing = [i,j,'XY1','XY2']
				if lpl[i].XY2 == lpl[j].XY2: comparing = [i,j,'XY2','XY2']
				if lpl[i].XY2 == lpl[j].XY1: comparing = [i,j,'XY2','XY1']
				# When the comparation is filled, a polyline exists
				if len(comparing) > 0: return comparing
		# No more lines non-routed:
		return False

	def enroute(self):
		c = True
		while c != False:
			lpl = self.line_list
			c = self.compare()
			if c == False: return True
			i = c[0]
			j = c[1]
			color = lpl[j].color
			thickness = lpl[j].thickness
			# Detect if line lpl[i] is a polyline
			try:
				lpl[i].XY
				iP = True
			except: iP = False
			# Detect if line lpl[j] is a polyline
			try:
				lpl[j].XY
				jP = True
			except: jP = False
			# The next code cascade create the line listing
			XY = []
			if c[2] == 'XY1' and c[3] == 'XY1':
				XY1,XY2 = lpl[i].XY2, lpl[j].XY2
				if iP and jP:
					for xy in reversed(lpl[i].XY): XY.append(xy)
					XY.append(lpl[i].XY1)
					for xy in lpl[j].XY: XY.append(xy)
				elif iP and not jP:
					for xy in reversed(lpl[i].XY): XY.append(xy)
					XY.append(lpl[i].XY1)
				elif not iP and jP:
					XY.append(lpl[i].XY1)
					for xy in lpl[j].XY: XY.append(xy)
				elif not iP and not jP:
					XY.append(lpl[i].XY1)
			if c[2] == 'XY1' and c[3] == 'XY2':
				XY1,XY2 = lpl[j].XY1, lpl[i].XY2
				if iP and jP:
					for xy in lpl[j].XY: XY.append(xy)
					XY.append(lpl[i].XY1)
					for xy in lpl[i].XY: XY.append(xy)
				elif iP and not jP:
					XY.append(lpl[i].XY1)
					for xy in lpl[i].XY: XY.append(xy)
				elif not iP and jP:
					for xy in lpl[j].XY: XY.append(xy)
					XY.append(lpl[i].XY1)
				elif not iP and not jP:
					XY.append(lpl[i].XY1)
			if c[2] == 'XY2' and c[3] == 'XY1':
				XY1,XY2 = lpl[i].XY1, lpl[j].XY2
				if iP and jP:
					for xy in lpl[i].XY: XY.append(xy)
					XY.append(lpl[i].XY2)
					for xy in lpl[j].XY: XY.append(xy)
				elif iP and not jP:
					for xy in lpl[i].XY: XY.append(xy)
					XY.append(lpl[i].XY2)
				elif not iP and jP:
					XY.append(lpl[i].XY2)
					for xy in lpl[j].XY: XY.append(xy)
				elif not iP and not jP:
					XY.append(lpl[i].XY2)
			if c[2] == 'XY2' and c[3] == 'XY2':
				XY1,XY2 = lpl[i].XY1, lpl[j].XY1
				if iP and jP:
					for xy in lpl[i].XY: XY.append(xy)
					XY.append(lpl[i].XY2)
					for xy in reversed(lpl[j].XY): XY.append(xy)
				elif iP and not jP:
					for xy in lpl[i].XY: XY.append(xy)
					XY.append(lpl[i].XY2)
				elif not iP and jP:
					XY.append(lpl[i].XY2)
					for xy in reversed(lpl[j].XY): XY.append(xy)
				elif not iP and not jP:
					XY.append(lpl[i].XY2)
			lpl.append(PolyLine(XY1, XY2, XY, color = self.color, thickness = self.thickness))
			del(lpl[i])
			del(lpl[j])



class PolyLine:

	def __init__(self, XY1, XY2, XY, color = None, thickness = None):
		self.XY1 = XY1
		self.XY2 = XY2
		self.XY = XY
		self.color = color
		self.thickness = thickness

	def draw(self):
		draw = '\\draw'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.thickness != None:
			draw += ' [line width = ' + str(self.thickness) + 'pt]'
		coor = '(' + str(self.XY1[0]) + ',' + str(self.XY1[1]) +')'
		for xy in self.XY:
			coor += '--(' + str(xy[0]) + ',' + str(xy[1]) +')'
		if self.XY1 == self.XY2: coor += '--cycle'
		else: coor += '--(' + str(self.XY2[0]) + ',' + str(self.XY2[1]) + ')'

		return draw + ' ' + coor + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY1, rotate, mirror)
		x2,y2 = rotate_and_mirror_XY(self.XY2, rotate, mirror)
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]
		XY = []
		for xy in self.XY:
			x,y = rotate_and_mirror_XY(xy, rotate, mirror)
			new_xy = [format(x,'.6f'),format(y,'.6f')]
			XY.append(new_xy)
		self.XY = XY

	def displace(self,XY):
		x1,y1 = float(self.XY1[0])+float(XY[0]),float(self.XY1[1])+float(XY[1])
		x2,y2 = float(self.XY2[0])+float(XY[0]),float(self.XY2[1])+float(XY[1])
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]
		sXY = []
		for xy in self.XY:
			x,y = float(xy[0])+float(XY[0]),float(xy[1])+float(XY[1])
			new_xy = [format(x,'.6f'),format(y,'.6f')]
			sXY.append(new_xy)
		self.XY = sXY




class Box:

	def __init__(self, XY1, XY2, color = None, thickness = None, fillcolor = None):
		self.XY1 = XY1
		self.XY2 = XY2
		self.fillcolor = fillcolor
		self.color = color
		self.thickness = thickness

	def draw(self):
		draw = '\\draw'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.fillcolor != None:
			draw += ' [fill = ' + str(self.fillcolor) + ']'
		if self.thickness != None:
			draw += ' [line width = ' + str(self.thickness) + 'pt]'
		coor = '(' + str(self.XY1[0]) + ',' + str(self.XY1[1]) +') rectangle (' + str(self.XY2[0]) + ',' + str(self.XY2[1]) + ')'
		return draw + ' ' + coor + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY1, rotate, mirror)
		x2,y2 = rotate_and_mirror_XY(self.XY2, rotate, mirror)
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]

	def displace(self,XY):
		x1,y1 = float(self.XY1[0])+float(XY[0]),float(self.XY1[1])+float(XY[1])
		x2,y2 = float(self.XY2[0])+float(XY[0]),float(self.XY2[1])+float(XY[1])
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]











class Circle:

	def __init__(self, XY, radius, color = None, thickness = None, fillcolor = None):
		self.XY = XY
		self.radius = radius
		self.fillcolor = fillcolor
		self.color = color
		self.thickness = thickness

	def draw(self):
		draw = '\\draw'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.fillcolor != None:
			draw += ' [fill = ' + str(self.fillcolor) + ']'
		if self.thickness != None:
			draw += ' [line width = ' + str(self.thickness) + 'pt]'
		coor = '(' + str(self.XY[0]) + ',' + str(self.XY[1]) +') circle (' + str(self.radius) + ')'
		return draw + ' ' + coor + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY, rotate, mirror)
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]

	def displace(self,XY):
		x1,y1 = float(self.XY[0])+float(XY[0]),float(self.XY[1])+float(XY[1])
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]









class Arc:

	def __init__(self, XY, radius, start_angle, sweep_angle, color = None, thickness = None, fillcolor = None):
		self.XY = XY
		self.radius = radius
		self.start_angle = start_angle
		self.sweep_angle = sweep_angle
		self.fillcolor = fillcolor
		self.color = color
		self.thickness = thickness

	def draw(self):
		draw = '\\draw'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.fillcolor != None:
			draw += ' [fill = ' + str(self.fillcolor) + ']'
		if self.thickness != None:
			draw += ' [line width = ' + str(self.thickness) + 'pt]'
		coor = '([shift = (' + str(self.start_angle) + ':' + str(self.radius) + ')] ' + str(self.XY[0]) + ',' + str(self.XY[1]) +') arc (' + str(self.start_angle) + ':' + str(float(self.start_angle)+float(self.sweep_angle)) + ':' + str(self.radius) + ')'
		return draw + ' ' + coor + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY, rotate, mirror)
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]
		a = rotate_and_mirror_angle(self.start_angle, rotate, mirror)
		self.start_angle = str(a)
		if mirror: self.sweep_angle = str(-float(self.sweep_angle))

	def displace(self, XY):
		x1,y1 = float(self.XY[0])+float(XY[0]),float(self.XY[1])+float(XY[1])
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]





class Node:

	def __init__(self, XY, text, size = 10, rotate = 0, alignment = 'centered', color = None, inner_sep = None, fillcolor = None, shape = None):
		self.XY = XY
		self.text = text
		self.size = size
		self.color = color
		self.shape = shape
		self.rotate = rotate
		self.fillcolor = fillcolor
		self.alignment = alignment
		self.inner_sep = inner_sep

	def draw(self):
		draw = '\\node'
		if self.color != None:
			draw += ' [color = ' + str(self.color) + ']'
		if self.fillcolor != None:
			draw += ' [fill = ' + str(self.fillcolor) + ']'
		if self.alignment != None:
			draw += ' [' + str(self.alignment) + ']'
		if self.shape != None:
			draw += ' [draw, ' + str(self.shape) + ']'
		if self.rotate != None:
			draw += ' [rotate = ' + str(self.rotate) + ']'
		if self.inner_sep != None:
			draw += ' [inner sep = ' + str(self.inner_sep) + ']'
		coor = 'at (' + str(self.XY[0]) + ',' + str(self.XY[1]) +')'
		text = '{\\scalebox{' + str(int(self.size)/20) + '}{' + str(self.text) + '}}'
		return draw + ' ' + coor + ' ' + text + ';' + '\n'

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY, rotate, mirror)
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]
		self.rotate = str(int(self.rotate) + int(rotate))
		# Mirror the alignment
		if mirror:
			lst = self.alignment.split(' ')
			if len(lst) > 1 and (int(rotate) == 0 or int(rotate) == 180):
				if lst[1] == 'left':
					lst[1] = 'right'
				elif lst[1] == 'right':
					lst[1] = 'left'
			elif len(lst) > 1 and (int(rotate) == 90 or int(rotate) == 270):
				if lst[0] == 'above':
					lst[0] = 'below'
				elif lst[0] == 'below':
					lst[0] = 'above'
			self.alignment = ' '.join(lst)

	def displace(self, XY):
		x1,y1 = float(self.XY[0])+float(XY[0]),float(self.XY[1])+float(XY[1])
		self.XY = [format(x1,'.6f'),format(y1,'.6f')]



class Pin:

	def __init__(self, XY1, XY2, color = None, headcolor = None, thickness = None, headthickness = 2):
		self.XY1 = XY1
		self.XY2 = XY2
		self.color = color
		self.headcolor = headcolor
		self.thickness = thickness
		self.headthickness = headthickness

	def draw(self):
		draw = Line(self.XY1,self.XY2,self.color,self.thickness).draw()
		draw += Circle(self.XY1,str(self.headthickness)+'pt',self.color,self.thickness,self.headcolor).draw()
		return draw

	def rotate_and_mirror(self, rotate, mirror):
		x1,y1 = rotate_and_mirror_XY(self.XY1, rotate, mirror)
		x2,y2 = rotate_and_mirror_XY(self.XY2, rotate, mirror)
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]

	def displace(self,XY):
		x1,y1 = float(self.XY1[0])+float(XY[0]),float(self.XY1[1])+float(XY[1])
		x2,y2 = float(self.XY2[0])+float(XY[0]),float(self.XY2[1])+float(XY[1])
		self.XY1 = [format(x1,'.6f'),format(y1,'.6f')]
		self.XY2 = [format(x2,'.6f'),format(y2,'.6f')]


class Component:

	def __init__(self, XY, tikz_shapes, rotate = 0, mirror = False):
		self.XY = XY
		self.tikz_shapes = tikz_shapes
		self.rotate = rotate
		self.mirror = mirror

	def draw(self):
		draw = ''
		self.rotate_and_mirror(self.rotate, self.mirror)
		self.displace(self.XY)
		for shape in self.tikz_shapes:
			draw += shape.draw()
		return draw

	def rotate_and_mirror(self, rotate, mirror):
		for shape in self.tikz_shapes:
			shape.rotate_and_mirror(self.rotate, self.mirror)

	def displace(self, XY):
		for shape in self.tikz_shapes:
			shape.displace(XY)

def rotate_and_mirror_XY(XY, rotate, mirror):
	x,y = float(XY[0]),float(XY[1])
	if int(rotate) == 0 and mirror:
		if mirror:
			x,y = -x,+y
	elif int(rotate) == 90:
		if mirror:
			x,y = +y,+x
		else:
			x,y = -y,+x
	elif int(rotate) == 180:
		if mirror:
			x,y = +x,-y
		else:
			x,y = -x,-y
	elif int(rotate) == 270:
		if mirror:
			x,y = -y,-x
		else:
			x,y = +y,-x
	return [x,y]

def rotate_and_mirror_angle(angle, rotate, mirror):
	a = float(angle)
	if int(rotate) == 90:
		a += 90
	elif int(rotate) == 180:
		a += 180
	elif int(rotate) == 270:
		a += 270
	if mirror:
		a = 180-a
	return a



class TikZComponent:

	def __init__(self, XY, tikz_scope, rotate = 0, mirror = False):
		self.XY = XY
		self.rotate = rotate
		self.mirror = mirror
		self.tikz_scope = tikz_scope

	def draw(self):
		rotate = self.rotate
		tikz_scope = self.tikz_scope
		XY = self.XY
		draw = '\\begin{scope}[shift = {(' + str(XY[0]) + ',' + str(XY[1]) + ')}'
		if rotate != 0:
			draw += ' ,rotate = ' + str(self.rotate)
		if self.mirror:
			draw += ' ,xscale = -1'
		draw += ']\n'
		# Mirror the alignment
		if self.mirror:
			notyet = True
			while notyet:
				last_tikz_scope = tikz_scope
				if (int(rotate) == 0 or int(rotate) == 180):
					tikz_scope.replace('&!left!&','right')
					tikz_scope.replace('&!right!&','left')
				elif (int(rotate) == 90 or int(rotate) == 270):
					tikz_scope.replace('&!above!&','below')
					tikz_scope.replace('&!below!&','above')
				if tikz_scope == last_tikz_scope: notyet = False
		tikz_scope.replace('&!rotate!&',str(self.rotate))
		draw += tikz_scope
		draw += '\\end{scope}\n'
		return draw




















#
