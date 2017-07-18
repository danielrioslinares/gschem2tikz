# gschem2tikz

This script converts a .sch from gEDA (gschem) schematic creator to tikz shapes. In order to use it you must execute in the root folder the next commands:

from core.Schematic import Schematic

file = 'untitled.sch'

config = 'config/config_default.ini'

directories = ['/usr/share/gEDA/sym/']

print( Schematic(file, config, directories).draw() )

where file is the absolute (or relative path) of the schematic, config is 'config/config_default.ini' in general and directories is a list of all directories where you have defined components for gschem.

This is a very early development, after a couple days I will create a GUI for being more user-friendly.
