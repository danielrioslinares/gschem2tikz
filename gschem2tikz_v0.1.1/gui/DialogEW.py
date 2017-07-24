#!/usr/bin/python

from gui.DialogUI import Ui_dialog_Dialog_is_DialogUI as DialogUI
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from core.Schematic import Schematic
from cfg.GuiConfig import GuiConfig
import os


class Ui_dialog_Dialog_is_DialogEW(DialogUI):

	DIRTYNAME = '<dirty>'
	DEFAULTNAME = 'default'

	def __init__(self):
		# This is the list of files to convert
		self.files = []

		# This is the list of directories where symbols are located
		self.directories = []

		# A GuiConfig for pass the configuration correctly
		self.gc = GuiConfig()

		# When an option is modified in the configuration, the preset is unknown
		self.dirty = None

	def setupUi(self, dialog_Dialog_is_DialogUI):
		DialogUI.setupUi(self,dialog_Dialog_is_DialogUI)
		self.setEventsUi(dialog_Dialog_is_DialogUI)
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.setColumnWidth(0,135)
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.setColumnWidth(1,50)
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.setColumnWidth(2,50)
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.setColumnWidth(3,50)

		self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.setColumnWidth(0,120)
		self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.setColumnWidth(1,80)
		self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.setColumnWidth(2,80)

		# Find all presets
		self.fillPresets()

		# First time preset
		self.widget_ComboBox_in_MainDialog_Preset_is_Preset.setCurrentIndex(self.widget_ComboBox_in_MainDialog_Preset_is_Preset.findText('default'))
		self.load_preset()
		self.dirty = False

	def setEventsUi(self, dialog_Dialog_is_DialogUI):

		###______[ Schematic selector zone ]______###
		self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_Run.clicked.connect(self.run)
		self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_AddSchematics.clicked.connect(self.addSchematics)
		self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_DeleteSchematic.clicked.connect(self.delSchematic)
		self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_DeleteSchematics.clicked.connect(self.clearSchematics)
		self.widget_PushButton_in_MainDialog_Preset_is_Load.clicked.connect(self.load_preset)
		self.widget_PushButton_in_MainDialog_Preset_is_Save.clicked.connect(self.save_preset)
		self.widget_PushButton_in_MainDialog_Preset_is_Delete.clicked.connect(self.delete)
		self.widget_PushButton_in_MainDialog_Preset_is_Refresh.clicked.connect(self.fillPresets)
		self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_AddAttribute.clicked.connect(self.addAttribute)
		self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_DelAttribute.clicked.connect(self.delAttribute)

		###______[ Main Tab widget ]______###
		# When tab is changed, refresh other tabs information:
		self.widget_TabWidget_in_MainDialog_is_MainTab.currentChanged.connect(self.tabChanged)

		###______[ Libraries tab ]______###
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_AddDirectory.clicked.connect(self.addDirectory)
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_DeleteDirectory.clicked.connect(self.delDirectory)
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeUp.clicked.connect(self.upDirectory)
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeDown.clicked.connect(self.downDirectory)
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeTop.clicked.connect(self.topDirectory)
		self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeBottom.clicked.connect(self.bottomDirectory)

		###______[ Color definitions tab ]______###
		self.widget_ToolButton_in_MainTab_ColorDefinitions_ColorTableControlsLayout_is_AddColor.clicked.connect(self.addColor)
		self.widget_ToolButton_in_MainTab_ColorDefinitions_ColorTableControlsLayout_is_DelColor.clicked.connect(self.delColor)

		###______[ Dirty preset ]______###
		## clicked
		self.widget_CheckBox_in_MainTab_General_OutputFileNameFormatBox_Layout_is_boolOriginalName.clicked.connect(self.dirtyPreset)
		self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveIndividualFile.clicked.connect(self.dirtyPreset)
		self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_Layout_is_boolSaveOriginalDirectory.clicked.connect(self.dirtyPreset)
		self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveAllFilesSameDirectory.clicked.connect(self.dirtyPreset)
		self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_DelAttribute.clicked.connect(self.dirtyPreset)
		self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_DelAttribute.clicked.connect(self.dirtyPreset)
		## editTextChanged
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor.editTextChanged.connect(self.dirtyPreset)
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor.editTextChanged.connect(self.dirtyPreset)
		## itemSelectionChanged
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.itemSelectionChanged.connect(self.dirtyPreset)
		self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.itemSelectionChanged.connect(self.dirtyPreset)
		self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.itemSelectionChanged.connect(self.dirtyPreset)

	'''______[ Event functions ]______'''

	###______[ Global ]______###

	# tabChanged() {void function(void)}
	# 	@connect : self.widget_TabWidget_in_MainDialog_is_MainTab
	# 	@target : self.widget_ComboBox_in_MainTab_Colors_Layout_is_str*
	#
	# Everytime tab is changed, the color list is refreshed
	def tabChanged(self):
		# Remove all unnamed colors definitions
		for i in reversed(range(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.rowCount())):
			if self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.item(i,0) == None:
				self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.removeRow(i)
		# Conserve the dirty state
		conserveDirty = self.dirty
		self.dirty = None
		# Consider the colors defined in combo boxes color tab
		colorComboBoxes = [self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor,
			self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor
			]
		text1 = []
		for cb in colorComboBoxes:
			text1.append(cb.currentText())
			cb.clear()

		text2 = []
		for i in range(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.rowCount()):
			text2.append(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.takeItem(i,0).text().replace(' ',''))
			self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.setItem(i,0,QtWidgets.QTableWidgetItem(text2[-1].replace(' ','')))

		for t1,cb in zip(text1,colorComboBoxes):
			cb.addItem(t1)
			for t2 in text2:
				if t2[:7] != 'FAILURE': cb.addItem(t2)
		self.dirty = conserveDirty

	# dirtyPreset() {void function(void)}
	# 	@connect : self.XXX
	# 	@target : self.widget_ComboBox_in_MainDialog_Preset_is_Preset
	#
	# As configuration is different from the preset, creates a new dirty preset
	def dirtyPreset(self):
		if self.dirty == False:
			self.dirty = True
			self.widget_ComboBox_in_MainDialog_Preset_is_Preset.addItem(self.DIRTYNAME)
			i = self.widget_ComboBox_in_MainDialog_Preset_is_Preset.findText(self.DIRTYNAME)
			self.widget_ComboBox_in_MainDialog_Preset_is_Preset.setCurrentIndex(i)

	# cleanPreset() {void function(void)}
	# 	@connect : self.XXX
	# 	@target : self.widget_ComboBox_in_MainDialog_Preset_is_Preset
	#
	# Everytime tab is changed, the color list is refreshed
	def cleanPreset(self):
		self.dirty = False
		i = self.widget_ComboBox_in_MainDialog_Preset_is_Preset.findText('<custom>')
		self.widget_ComboBox_in_MainDialog_Preset_is_Preset.removeItem(i)

	###______[ Schematic selector zone ]______###

	# run() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_Run
	#
	# Convert all files
	def run(self):
		schematics = []
		self.set_operation('Working')
		if self.gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveallfilessamedirectory','bool'):
			directory = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select the folder', os.getenv('HOME'), QtWidgets.QFileDialog.ShowDirsOnly)
		else:
			directory = os.getenv('HOME')
		numberOfFiles = len(self.get_files())
		prefix = self.gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strprefix')
		suffix = self.gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strsuffix')
		self.set_progress(0)
		for f,i in zip(self.get_files(),range(numberOfFiles)):
			config = self.get_selectedPreset()
			directories = self.get_directories()
			sch = Schematic(f, config, directories, self.gc)
			if self.gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveoriginaldirectory','bool'):
				filename = sch.get_file().replace('.sch','').replace('.sym','')
				filename = '/'.join(filename.split('/')[:-1]) + '/' + prefix + filename.split('/')[-1] + suffix + '.tikz'
			elif self.gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveindividualfile','bool'):
				path = sch.get_file().split('/')
				del(path[-1])
				path = '/'.join(path)
				filename,_ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save schematic...', path + '/' + prefix + f.split('/')[-1].replace('.sch','.tikz').replace('.sym','.tikz') + suffix, 'tikz file (*.tikz);;all files (*)')
			elif self.gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveallfilessamedirectory','bool'):
				filename = directory + '/' + sch.get_file().split('/')[-1].replace('.sch','').replace('.sym','')
				filename = '/'.join(filename.split('/')[:-1]) + '/' + self.gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strprefix') + filename.split('/')[-1] + self.gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strsuffix') + '.tikz'
			self.set_progress(int(100*(i+1)/numberOfFiles))
			if filename != '':
				tikzFile = open(filename,"w")
				if self.gc.get_cfg('maintab/general/otherbox/layout','boolincludetikzenvironment','bool'):
					tikzFile.write('\\begin{tikzpicture}\n' + sch.draw() + '\\end{tikzpicture}')
				else:
					tikzFile.write(sch.draw())
				tikzFile.close()
		self.set_operation('Done!')

	# delete() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_Run
	#
	# Remove the current preset
	def delete(self):
		try:
			os.remove(self.get_selectedPreset())
			self.fillPresets()
		except:
			pass

	# addSchematics() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_AddSchematics
	# 	@target : self.widget_ListWidget_in_MainDialog_is_SchematicList
	#
	# Pops up a open file dialog and add a list of absolute paths to @target
	def addSchematics(self):
		filenames,_ = QtWidgets.QFileDialog.getOpenFileNames(None, 'Open gschem schematics', os.getenv('HOME'), 'gschem schematic (*.sch);;gschem symbol (*.sym);;all files (*)')
		for filename in filenames:
			addit = True
			for f in self.files:
				if f == filename: addit = False
			if addit:
				self.widget_ListWidget_in_MainDialog_is_SchematicList.addItem(QtWidgets.QListWidgetItem(filename))
				self.add_file(filename)

	# delSchematic() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_DeleteSchematic
	# 	@target : self.widget_ListWidget_in_MainDialog_is_SchematicList
	#
	# Detect the current selected item in @target and removes it
	def delSchematic(self):
		try:
			i = self.widget_ListWidget_in_MainDialog_is_SchematicList.currentRow()
			self.del_file(i)
			item = self.widget_ListWidget_in_MainDialog_is_SchematicList.takeItem(i)
			item = None
		except:
			pass

	# clearSchematics() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_DeleteSchematics
	# 	@target : self.widget_ListWidget_in_MainDialog_is_SchematicList
	#
	# Clears @target items
	def clearSchematics(self):
		self.clear_files()
		self.widget_ListWidget_in_MainDialog_is_SchematicList.clear()

	# fillPresets() {void function(void)}
	# 	@connect : self.widget_PushButton_in_MainDialog_Preset_is_Refresh
	# 	@target : self.widget_ComboBox_in_MainDialog_Preset_is_Preset
	#
	# Refreshes all presets in @target by pressing @connect
	def fillPresets(self):
		dirty = self.dirty
		self.dirty = None
		self.widget_ComboBox_in_MainDialog_Preset_is_Preset.clear()
		for item in self.gc.get_presetsFilenames():
			self.widget_ComboBox_in_MainDialog_Preset_is_Preset.addItem(item.replace('.ini',''))
		if dirty == True:
			self.widget_ComboBox_in_MainDialog_Preset_is_Preset.addItem(self.DIRTYNAME)
			self.widget_ComboBox_in_MainDialog_Preset_is_Preset.setCurrentIndex(self.widget_ComboBox_in_MainDialog_Preset_is_Preset.findText(self.DIRTYNAME))
		self.dirty = dirty

	###______[ Libraries tab ]______###

	# addDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_AddDirectory
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Refreshes all presets in @target by pressing @connect
	def addDirectory(self):
		directory = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select the library folder', os.getenv('HOME'), QtWidgets.QFileDialog.ShowDirsOnly)
		if directory[-1] != '/': directory += '/'
		if directory[0] == ' ' : del(directory[0])
		addit = True
		if len(self.directories) != 0:
			for d in self.directories:
				if d == directory:
					addit = False
		if addit:
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.addItem(QtWidgets.QListWidgetItem(directory))
			self.add_directory(directory)

	# delDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_DeleteDirectory
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Detect the current selected item in @target and removes it
	def delDirectory(self):
		i = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.currentRow()
		self.del_directory(i)
		item = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.takeItem(i)
		item = None

	# upDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeUp
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Priorize up a directory for the list @target
	def upDirectory(self):
		i = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.currentRow()
		if i != 0:
			item = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.takeItem(i)
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.insertItem(i-1,item)
			self.directories.insert(i-1,self.directories[i])
			del(self.directories[i+1])
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.setCurrentRow(i-1)

	# downDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeDown
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Priorize down a directory for the list @target
	def downDirectory(self):
		i = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.currentRow()
		m = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.count()-1
		if i != m:
			item = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.takeItem(i)
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.insertItem(i+1,item)
			self.directories.insert(i+1,self.directories[i])
			del(self.directories[i])
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.setCurrentRow(i+1)

	# topDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeTop
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Priorize to the top a directory for the list @target
	def topDirectory(self):
		i = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.currentRow()
		m = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.count()-1
		if i != 0:
			item = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.takeItem(i)
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.insertItem(0,item)
			self.directories.insert(0,self.directories[i])
			del(self.directories[i+1])
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.setCurrentRow(0)

	# bottomDirectory() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Libraries_GschemSymbolsDirectories_ControlPanelLayout_is_PriorizeBottom
	# 	@target : self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList
	#
	# Priorize to the bottom a directory for the list @target
	def bottomDirectory(self):
		i = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.currentRow()
		m = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.count()-1
		if i != m:
			item = self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.takeItem(i)
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.insertItem(m,item)
			self.directories.insert(m,self.directories[i])
			del(self.directories[i])
			self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.setCurrentRow(m)

	###______[ Color definitions tab ]______###

	# addColor() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_ColorDefinitions_ColorTableControlsLayout_is_AddColor
	# 	@target : self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable
	#
	# Adds a row in @target by pressing @connect
	def addColor(self):
		table = self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable
		i = table.currentRow()+1
		table.insertRow(i)
		for j in range(3):
			self.create_doubleSpinBoxForTable(table,i,j+1)
		"""
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.insertRow(0)
		"""
	# delColor() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_ColorDefinitions_ColorTableControlsLayout_is_DelColor
	# 	@target : self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable
	#
	# Removes a row in @target by pressing @connect
	def delColor(self):
		i = self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.currentRow()
		self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.removeRow(i)

	# addAttribute() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_AddAttribute
	# 	@target : self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable
	#
	# Adds a row in @target by pressing @connect
	def addAttribute(self):
		table = self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable
		i = table.currentRow()+1
		table.insertRow(i)
		self.create_checkBoxForTable(table,i,1)
		self.create_checkBoxForTable(table,i,2)

	# get_checkBoxStateForTable() {bool function(PyQt5.QtWidgets.QTableWidget table, int row, int col)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@target : table
	#
	# Returns the state of a checkbox created with self.create_checkBoxForTable on @target
	def get_checkBoxStateForTable(self,table,row,col):
		item = table.cellWidget(row,col)
		return True if item.checkState() == QtCore.Qt.Checked else False

	# set_checkBoxStateForTable() {void function(PyQt5.QtWidgets.QTableWidget table, int row, int col)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@target : table
	#
	# Sets the state of a checkbox created with self.create_checkBoxForTable on @target
	def set_checkBoxStateForTable(self,table,row,col,state):
		item = table.cellWidget(row,col)
		if state:
			item.setCheckState(QtCore.Qt.Checked)
		else:
			item.setCheckState(QtCore.Qt.Unchecked)

	# get_checkBoxStateForTable() {bool function(PyQt5.QtWidgets.QTableWidget table, int row, int col)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@target : table
	#
	# Returns the state of a checkbox created with self.create_checkBoxForTable on @target
	def get_doubleSpinBoxForTable(self,table,row,col):
		item = table.cellWidget(row,col)
		return item.value()

	# set_checkBoxStateForTable() {void function(PyQt5.QtWidgets.QTableWidget table, int row, int col, str val)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@param str val : value to set
	# 	@target : table
	#
	# Sets the state of a checkbox created with self.create_checkBoxForTable on @target
	def set_doubleSpinBoxForTable(self,table,row,col,val):
		item = table.cellWidget(row,col)
		item.setValue(float(val))

	# create_checkBoxForTable() {<QtWidgets.QTableWidgetItem object> function(void)}
	# 	@target : table
	#
	# Sets in @target for row and col checkbox for @target state
	def create_checkBoxForTable(self,table,row,col):
		checkbox = QtWidgets.QCheckBox()
		table.setCellWidget(row,col,checkbox)
		return checkbox

	# create_doubleSpinBoxForTable() {<QtWidgets.QTableWidgetItem object> function(void)}
	# 	@target : table
	#
	# Sets in @target for row and col doubleSpinBox for @target
	def create_doubleSpinBoxForTable(self,table,row,col):
		doublespin = QtWidgets.QDoubleSpinBox()
		doublespin.setMaximum(1.0)
		doublespin.setMinimum(0.0)
		doublespin.setSingleStep(0.05)
		table.setCellWidget(row,col,doublespin)
		return doublespin

	# get_textForTable() {bool function(PyQt5.QtWidgets.QTableWidget table, int row, int col)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@target : table
	#
	# Returns the text of a cell created with self.create_checkBoxForTable on @target
	def get_textForTable(self,table,row,col):
		return table.item(row,col).text()


	# set_textForTable() {bool function(PyQt5.QtWidgets.QTableWidget table, int row, int col)}
	# 	@param PyQt5.QtWidgets.QTableWidget table : table from where get the check state
	# 	@param int row : row of the table
	# 	@param int col : column of the table
	# 	@param str text : text to be setted
	# 	@target : table
	#
	# Set the text on a cell of @target
	def set_textForTable(self,table,row,col,text):
		table.setItem(row,col,QtWidgets.QTableWidgetItem(text))


	# delAttribute() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainTab_Attributes_AttributesTableControlsLayout_is_DelAttribute
	# 	@target : self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable
	#
	# Removes a row in @target by pressing @connect
	def delAttribute(self):
		i = self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.currentRow()
		self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.removeRow(i)

	'''______[ Load and save configuration ]______'''

	# load_preset() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_Run
	#
	# Loads the preset selected in combo box
	def load_preset(self):
		preset = self.widget_ComboBox_in_MainDialog_Preset_is_Preset.currentText()
		gc = self.gc
		gc.set_preset(gc.presets_directory + '/' + preset + '.ini')
		###______[ General ]______###
		# Output file name format box
		self.widget_LineEdit_in_MainTab_General_OutputFileNameFormatBox_Layout_is_strPrefix.setText(gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strprefix','str'))
		self.widget_CheckBox_in_MainTab_General_OutputFileNameFormatBox_Layout_is_boolOriginalName.setChecked(gc.get_cfg('maintab/general/outputfilenameformatbox/layout','booloriginalname','bool'))
		self.widget_LineEdit_in_MainTab_General_OutputFileNameFormatBox_Layout_is_strSuffix.setText(gc.get_cfg('maintab/general/outputfilenameformatbox/layout','strsuffix','str'))
		# Output file save mode box
		if gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveoriginaldirectory','bool'): self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_Layout_is_boolSaveOriginalDirectory.toggle()
		if gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveindividualfile','bool'): self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveIndividualFile.toggle()
		if gc.get_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveallfilessamedirectory','bool'): self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveAllFilesSameDirectory.toggle()
		# Other
		self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolLetGschemSetAttributesToShow.setChecked(gc.get_cfg('maintab/general/otherbox/layout','boolletgschemsetattributestoshow','bool'))
		self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolIncludeTikZEnvironment.setChecked(gc.get_cfg('maintab/general/otherbox/layout','boolincludetikzenvironment','bool'))
		self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolShowPinHead.setChecked(gc.get_cfg('maintab/general/otherbox/layout','boolshowpinhead','bool'))

		###______[ Libraries ]______###
		directories = gc.get_cfg('maintab/libraries/dependanceoptionsbox/layout','listgschemsymbolsdirectories','list')

		self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.clear()
		self.directories.clear()

		for directory in directories[0]:
			addit = True
			for d in self.directories:
				if d == directory: addit = False
			if addit:
				self.widget_ListWidget_in_MainTab_Libraries_GschemSymbolsDirectoriesBox_is_DirectoryList.addItem(QtWidgets.QListWidgetItem(directory))
				self.add_directory(directory)

		###______[ Thickness ]______###
		# Schematic line width box
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatBus.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatbus','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatNet.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatnet','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatBoxLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatboxline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatCircleLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatcircleline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatArcLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatarcline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatPinLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatPinHeadLine.setValue(gc.get_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinheadline','float'))
		# Component line width box
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatBus.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatbus','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatNet.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatnet','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatBoxLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatboxline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatCircleLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatcircleline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatArcLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatarcline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatPinLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinline','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatPinHeadLine.setValue(gc.get_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinheadline','float'))
		# Text alignment distance box
		self.widget_DoubleSpinBox_in_MainTab_Thickness_TextAlignmentDistanceBox_SchematicLayout_is_floatSchematic.setValue(gc.get_cfg('maintab/thickness/textalignmentdistancebox/schematiclayout','floatschematic','float'))
		self.widget_DoubleSpinBox_in_MainTab_Thickness_TextAlignmentDistanceBox_ComponentLayout_is_floatComponent.setValue(gc.get_cfg('maintab/thickness/textalignmentdistancebox/componentlayout','floatcomponent','float'))

		###______[ Colors ]______###
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground.addItem(gc.get_cfg('maintab/colors/layout','strbackground','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin.addItem(gc.get_cfg('maintab/colors/layout','strpin','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint.addItem(gc.get_cfg('maintab/colors/layout','strnetendpoint','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet.addItem(gc.get_cfg('maintab/colors/layout','strnet','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic.addItem(gc.get_cfg('maintab/colors/layout','strgraphic','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute.addItem(gc.get_cfg('maintab/colors/layout','strattribute','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble.addItem(gc.get_cfg('maintab/colors/layout','strlogicbubble','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint.addItem(gc.get_cfg('maintab/colors/layout','strgridpoint','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute.addItem(gc.get_cfg('maintab/colors/layout','strdetachedattribute','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection.addItem(gc.get_cfg('maintab/colors/layout','strselection','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox.addItem(gc.get_cfg('maintab/colors/layout','strboundingbox','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox.addItem(gc.get_cfg('maintab/colors/layout','strzoombox','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText.addItem(gc.get_cfg('maintab/colors/layout','strtext','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus.addItem(gc.get_cfg('maintab/colors/layout','strbus','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke.addItem(gc.get_cfg('maintab/colors/layout','strstroke','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock.addItem(gc.get_cfg('maintab/colors/layout','strlock','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction.addItem(gc.get_cfg('maintab/colors/layout','strnetjunction','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor.addItem(gc.get_cfg('maintab/colors/layout','strmeshgridmayor','str'))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor.addItem(gc.get_cfg('maintab/colors/layout','strmeshgridminor','str'))
		# Find item
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground.findText(gc.get_cfg('maintab/colors/layout','strbackground','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin.findText(gc.get_cfg('maintab/colors/layout','strpin','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint.findText(gc.get_cfg('maintab/colors/layout','strnetendpoint','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet.findText(gc.get_cfg('maintab/colors/layout','strnet','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic.findText(gc.get_cfg('maintab/colors/layout','strgraphic','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute.findText(gc.get_cfg('maintab/colors/layout','strattribute','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble.findText(gc.get_cfg('maintab/colors/layout','strlogicbubble','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint.findText(gc.get_cfg('maintab/colors/layout','strgridpoint','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute.findText(gc.get_cfg('maintab/colors/layout','strdetachedattribute','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection.findText(gc.get_cfg('maintab/colors/layout','strselection','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox.findText(gc.get_cfg('maintab/colors/layout','strboundingbox','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox.findText(gc.get_cfg('maintab/colors/layout','strzoombox','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText.findText(gc.get_cfg('maintab/colors/layout','strtext','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus.findText(gc.get_cfg('maintab/colors/layout','strbus','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke.findText(gc.get_cfg('maintab/colors/layout','strstroke','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock.findText(gc.get_cfg('maintab/colors/layout','strlock','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction.findText(gc.get_cfg('maintab/colors/layout','strnetjunction','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor.findText(gc.get_cfg('maintab/colors/layout','strmeshgridmayor','str')))
		self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor.setCurrentIndex(self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor.findText(gc.get_cfg('maintab/colors/layout','strmeshgridminor','str')))

		###______[ Color definitions ]______###
		for i in range(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.rowCount()): self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.removeRow(0)
		colors = gc.get_cfg('maintab/colordefinitions/layout','colortable','list')
		for i in range(len(colors)):
			self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.insertRow(i)
			for j in range(3):
				self.create_doubleSpinBoxForTable(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable,i,j+1)
				self.set_doubleSpinBoxForTable(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable,i,j+1,colors[i][j+1])
			self.set_textForTable(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable,i,0,colors[i][0])

		###______[ Attributes ]______###
		for i in range(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.rowCount()): self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.removeRow(0)
		attributes = gc.get_cfg('maintab/attributes','attributestable','list')
		for i in range(len(attributes)):
			self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.insertRow(i)
			for j in range(2):
				self.create_checkBoxForTable(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable,i,j+1)
				state = True if attributes[i][j+1] == 'True' or attributes[i][j+1] == 'True ' else False
				self.set_checkBoxStateForTable(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable,i,j+1,state)
			self.set_textForTable(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable,i,0,attributes[i][0])

		###______[ Finally, clean the preset ]______###
		self.cleanPreset()

	# save_preset() {void function(void)}
	# 	@connect : self.widget_ToolButton_in_MainDialog_SchematicListControlLayout_is_Run
	#
	# Convert all files
	def save_preset(self):
		if self.get_selectedPreset('name') == self.DIRTYNAME: return 0
		self.cleanPreset()
		gc = self.gc
		###______[ General ]______###
		# Output file name format box
		gc.set_cfg('maintab/general/outputfilenameformatbox/layout','strprefix',self.widget_LineEdit_in_MainTab_General_OutputFileNameFormatBox_Layout_is_strPrefix.text())
		gc.set_cfg('maintab/general/outputfilenameformatbox/layout','booloriginalname',str(self.widget_CheckBox_in_MainTab_General_OutputFileNameFormatBox_Layout_is_boolOriginalName.isChecked()))
		gc.set_cfg('maintab/general/outputfilenameformatbox/layout','strsuffix',self.widget_LineEdit_in_MainTab_General_OutputFileNameFormatBox_Layout_is_strSuffix.text())
		# Output file save mode box
		gc.set_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveoriginaldirectory', self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_Layout_is_boolSaveOriginalDirectory.isChecked())
		gc.set_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveindividualfile', self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveIndividualFile.isChecked())
		gc.set_cfg('maintab/general/outputfilesavemodebox/layout','boolsaveallfilessamedirectory', self.widget_VerticalLayout_in_MainTab_General_OutputFileSaveModeBox_is_Layout_is_boolSaveAllFilesSameDirectory.isChecked())
		# Other
		gc.set_cfg('maintab/general/otherbox/layout','boolletgschemsetattributestoshow', self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolLetGschemSetAttributesToShow.isChecked())
		gc.set_cfg('maintab/general/otherbox/layout','boolincludetikzenvironment', self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolIncludeTikZEnvironment.isChecked())
		gc.set_cfg('maintab/general/otherbox/layout','boolshowpinhead', self.widget_CheckBox_in_MainTab_General_OutputFileNameFormat_Layout_is_boolShowPinHead.isChecked())

		###______[ Libraries ]______###
		# Dependance options box
		gc.set_cfg('maintab/libraries/dependanceoptionsbox/layout','listgschemsymbolsdirectories', str(self.directories))

		###______[ Thickness ]______###
		# Schematic line width box
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatLine.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatbus', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatBus.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatnet', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatNet.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatboxline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatBoxLine.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatcircleline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatCircleLine.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatarcline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatArcLine.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatPinLine.value())
		gc.set_cfg('maintab/thickness/schematiclinewidthbox/layout','floatpinheadline', self.widget_DoubleSpinBox_in_MainTab_Thickness_SchematicLineWidthBox_Layout_is_floatPinHeadLine.value())
		# Component line width box
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatLine.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatbus', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatBus.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatnet', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatNet.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatboxline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatBoxLine.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatcircleline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatCircleLine.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatarcline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatArcLine.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatPinLine.value())
		gc.set_cfg('maintab/thickness/componentlinewidthbox/layout','floatpinheadline', self.widget_DoubleSpinBox_in_MainTab_Thickness_ComponentLineWidthBox_Layout_is_floatPinHeadLine.value())
		# Text alignment distance box
		gc.set_cfg('maintab/thickness/textalignmentdistancebox/schematiclayout','floatschematic', self.widget_DoubleSpinBox_in_MainTab_Thickness_TextAlignmentDistanceBox_SchematicLayout_is_floatSchematic.value())
		gc.set_cfg('maintab/thickness/textalignmentdistancebox/componentlayout','floatcomponent', self.widget_DoubleSpinBox_in_MainTab_Thickness_TextAlignmentDistanceBox_ComponentLayout_is_floatComponent.value())

		###______[ Colors ]______###
		gc.set_cfg('maintab/colors/layout','strbackground', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBackground.currentText())
		gc.set_cfg('maintab/colors/layout','strpin', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strPin.currentText())
		gc.set_cfg('maintab/colors/layout','strnetendpoint', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetEndpoint.currentText())
		gc.set_cfg('maintab/colors/layout','strnet', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNet.currentText())
		gc.set_cfg('maintab/colors/layout','strgraphic', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGraphic.currentText())
		gc.set_cfg('maintab/colors/layout','strattribute', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strAttribute.currentText())
		gc.set_cfg('maintab/colors/layout','strlogicbubble', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLogicBubble.currentText())
		gc.set_cfg('maintab/colors/layout','strgridpoint', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strGridPoint.currentText())
		gc.set_cfg('maintab/colors/layout','strdetachedattribute', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strDetachedAttribute.currentText())
		gc.set_cfg('maintab/colors/layout','strselection', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strSelection.currentText())
		gc.set_cfg('maintab/colors/layout','strboundingbox', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBoundingBox.currentText())
		gc.set_cfg('maintab/colors/layout','strzoombox', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strZoomBox.currentText())
		gc.set_cfg('maintab/colors/layout','strtext', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strText.currentText())
		gc.set_cfg('maintab/colors/layout','strbus', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strBus.currentText())
		gc.set_cfg('maintab/colors/layout','strstroke', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strStroke.currentText())
		gc.set_cfg('maintab/colors/layout','strlock', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strLock.currentText())
		gc.set_cfg('maintab/colors/layout','strnetjunction', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strNetJunction.currentText())
		gc.set_cfg('maintab/colors/layout','strmeshgridmayor', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMayor.currentText())
		gc.set_cfg('maintab/colors/layout','strmeshgridminor', self.widget_ComboBox_in_MainTab_Colors_Layout_is_strMeshGridMinor.currentText())

		###______[ Color definitions ]______###
		colors = []
		for i in range(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable.rowCount()):
			t = [self.get_textForTable(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable,i,0)]
			c = [self.get_doubleSpinBoxForTable(self.widget_TableWidget_in_MainTab_ColorDefinitions_is_ColorTable,i,j+1) for j in range(3)]
			colors.append(t + c)
		gc.set_cfg('maintab/colordefinitions/layout','colortable',str(colors))

		###______[ Attributes ]______###
		attributes = []
		for i in range(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable.rowCount()):
			t = [self.get_textForTable(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable,i,0)]
			a = [self.get_checkBoxStateForTable(self.widget_TableWidget_in_MainTab_Attributes_is_AttributeTable,i,j+1) for j in range(2)]
			attributes.append(t + a)
		gc.set_cfg('maintab/attributes','attributestable',str(attributes))

		###______[ Save the preset ]______###
		# filename,_ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save preset', gc.presets_directory, 'preset file (*.ini);;all files (*)')
		preset = self.widget_ComboBox_in_MainDialog_Preset_is_Preset.currentText()

		filename = gc.presets_directory + '/' + preset + '.ini'
		gc.write_cfg( filename )

		self.fillPresets()
		i = self.widget_ComboBox_in_MainDialog_Preset_is_Preset.findText(preset)
		self.widget_ComboBox_in_MainDialog_Preset_is_Preset.setCurrentIndex(i)

		###______[ Load the preset ]______###
		self.load_preset()

	'''______[ Setters & getters ]______'''

	# set_progress(value) {void function(int value)}
	# 	@param value : percentage of the progress bar
	#
	# Move the progress bar widget
	def set_progress(self, value):
		self.widget_ProgressBar_in_MainDialog_StatusLayout_is_ProgressBar.setProperty("value", value)

	# set_operation(operation) {void function(str operation)}
	# 	@param operation : status label
	#
	# Sets the operation mode in the status
	def set_operation(self, operation):
		self.widget_Label_in_MainDialog_StatusLayout_is_CurrentSchematic.setText(operation)

	# add_file(filepath) {void function(str filepath)}
	# 	@param filepath : is the absolute path of the file to add
	#
	# Add a new file to the files
	def add_file(self, filepath): self.files.append(filepath)

	# add_directory(directory) {void function(str directory)}
	# 	@param directory : is the absolute path of the file to add
	#
	# Add a new directory to the directories
	def add_directory(self, directory): self.directories.append(directory)

	# del_file(i) {void function(int i)}
	#
	# Removes from the list of directories the file with index i
	def del_directory(self, i): del(self.directories[i])

	# get_directories() {void function(void)}
	#
	# Returns the list of directories
	def get_directories(self): return self.directories

	# clear_directories(i) {void function(void)}
	#
	# Removes from the list of directoties all the files
	def clear_directories(self): self.directories = []

	# del_file(i) {void function(int i)}
	#
	# Removes from the list of files the file with index i
	def del_file(self, i): del(self.files[i])

	# clear_files(i) {void function(void)}
	#
	# Removes from the list of files all the files
	def clear_files(self): self.files = []

	# get_files() {list<str> function(void)}
	#
	# Returns all files to convert
	def get_files(self): return self.files

	# get_selectedPreset(mode) {str function(str mode)}
	# 	@param mode : if mode == 'name' return only name of the preset
	#
	# Returns the absolute path of the current preset
	def get_selectedPreset(self,mode = ''):
		if mode == 'name':
			return self.widget_ComboBox_in_MainDialog_Preset_is_Preset.currentText()
		if self.widget_ComboBox_in_MainDialog_Preset_is_Preset.currentText() != self.DEFAULTNAME:
			return self.gc.presets_directory + '/' + self.widget_ComboBox_in_MainDialog_Preset_is_Preset.currentText() + '.ini'
		else:
			return None










# EOF
