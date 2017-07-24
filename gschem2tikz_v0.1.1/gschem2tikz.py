#!/usr/bin/python

"""
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""




# GUI modules and packages
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from gui.DialogUI import Ui_dialog_Dialog_is_DialogUI as DialogUI
from gui.DialogEW import Ui_dialog_Dialog_is_DialogEW as DialogEW

from core.Schematic import Schematic










# First, create the app
app = QtWidgets.QApplication(sys.argv)

# With the application created, create the dialog and...
dia = QtWidgets.QDialog()

# ...setup the graphical user interface and the event wrapper (DialogEW)
gui = DialogEW()
gui.setupUi(dia)

# Show the dialog
dia.show()

# When the dialog is closed, finish the application
sys.exit(app.exec_())















































#
