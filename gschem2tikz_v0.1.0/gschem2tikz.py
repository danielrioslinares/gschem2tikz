#!/usr/bin/python



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
