#!/usr/bin/python

from core.Schematic import Schematic


file = 'untitled.sch'
config = 'config/config_default.ini'
directories = ['/usr/share/gEDA/sym/']

print(
	Schematic(file, config, directories).draw()
	)









#
