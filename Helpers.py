#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx

class DataSize(wx.Dialog):

	def __init__(self, parent, id, minimum, maximum, title):
		wx.Dialog.__init__(self, parent, id, title, size=(350, 200), style= wx.THICK_FRAME|wx.OK)

		self.minimum = minimum
		self.maximum = maximum
		font_bottom = wx.Font(8.5, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')

		self.v_box_min = wx.BoxSizer(wx.HORIZONTAL)
                self.min_value = wx.StaticText(self, 0, "Minimum Value",)
                self.min_value_text = wx.TextCtrl(self, 0,)
                self.v_box_min.Add(self.min_value, 0, wx.EXPAND|wx.ALL, 4)
                self.v_box_min.Add(self.min_value_text, 0, wx.EXPAND|wx.ALL, 4)

		
		self.v_box_max = wx.BoxSizer(wx.HORIZONTAL)
		self.max_value = wx.StaticText(self, 0, "Maximum Value")
                self.max_value_text = wx.TextCtrl(self, 0,)
                self.v_box_max.Add(self.max_value, 0, wx.EXPAND|wx.ALL, 4)
                self.v_box_max.Add(self.max_value_text, 0, wx.EXPAND|wx.ALL, 4)
                
                self.min_value.SetFont(font_bottom)
                self.max_value.SetFont(font_bottom)

                self.min_value_text.SetValue(str(self.minimum))
                self.max_value_text.SetValue(str(self.maximum))
		

		btnOk = wx.Button(self, wx.ID_OK)
		btnCancel = wx.Button(self, wx.ID_CANCEL)

		self.btnSizer = wx.StdDialogButtonSizer()
		self.btnSizer.AddButton(btnOk)
		self.btnSizer.AddButton(btnCancel)
		self.btnSizer.Realize()
		
		self.main = wx.BoxSizer(wx.VERTICAL)
		self.main.Add(self.v_box_min, 0, wx.EXPAND|wx.ALL, 2)
		self.main.Add(self.v_box_max, 0, wx.EXPAND|wx.ALL, 2)
		self.main.Add(self.btnSizer, 0, wx.EXPAND|wx.ALL|wx.ALIGN_BOTTOM, 2)
		self.SetSizer(self.main)

		self.Center()


class ChangeBaseAxis(wx.Dialog):
	"""
	This class is used to change the base axis for the plotting of one dimensional plots
	The default base axis used to draw one dimensional plots is normal python range i.e number of data points to be plotted
	Arguments:
		parent:
			parent of this dialog box, which in this case is the maain wx.Frame
		base_axis:
			
	
	
	Class variables:
		checkboxes:
			List of the checkbox corresponding to each variable present in the data
		checkbox:
			The checkbox type(tuple) which has the checkbox being selected


	"""
	def __init__(self, parent, base_axis, data):
		wx.Dialog.__init__(self, parent, 0, size=(500, 400), style= wx.THICK_FRAME|wx.OK)
		
		self.base_axis = base_axis
		self.checkboxes = list()
		self.data = data
		

		if self.base_axis:
			self.text = "This dialogue box will change the base axis for the one diemsional plots, right now the base axis is %s"%self.base_axis.upper()
		else:
			self.text = "This dialogue box will change the base axis for the one diemsional plots, right now the base axis is %s"%"NORMAL PYTHON RANGE"


		self.checkbox = None	
		self.selected_checkboxes = list()
		self.scroll = wx.PyScrolledWindow(self, -1,)  
		self.panel = wx.Panel(self.scroll, -1)
		
		self.grid_sizer = wx.FlexGridSizer(len(self.data.columns), 2, 0, 2)
		self.grid_sizer.Add(wx.StaticText(self.panel, -1, self.text))
		self.grid_sizer.Add((20, 20))	
		self.populate_variables()


		btnOk = wx.Button(self.panel, wx.ID_OK)
		btnCancel = wx.Button(self.panel, wx.ID_CANCEL)

		self.btnSizer = wx.StdDialogButtonSizer()
		self.btnSizer.AddButton(btnOk)
		self.btnSizer.AddButton(btnCancel)
		self.btnSizer.Realize()
		
		self.box = wx.BoxSizer(wx.VERTICAL)
		self.box.Add(self.grid_sizer, proportion=1, flag=wx.ALL, border=20 )
		self.box.Add(self.btnSizer)
		
		self.panel.SetSizer(self.box)
		self.panel.SetAutoLayout( True )
		self.panel.Layout()
		self.panel.Fit()  

		self.Center()
		self.frmPanelWid, self.frmPanelHgt = self.panel.GetSize()
		self.unit = 1
		self.scroll.SetScrollbars(self.unit, self.unit, self.frmPanelWid/self.unit, self.frmPanelHgt/self.unit )



	def populate_variables(self):
		"""
		Variables:
			variable_description:
				type(string) which was made by joining sepereted by comma, the first three values of the variables present
				in the data
		This also appends the checkboxes list, with each and every checkbox created corresponding to each and every variable present 
		in the data
		"""
		
		x = 20
		y = 20
		for integer, variable  in enumerate(self.data.columns):
			sample_variable_data = [str(i) for i in self.data[variable].values[0:3]]
			label = ",  ".join(sample_variable_data)

			checkbox= wx.CheckBox(self.panel, integer, variable, pos=(x+5, y))
			self.grid_sizer.Add(checkbox)
			if variable == self.base_axis:
				checkbox.SetValue(True)
			self.checkboxes.append(checkbox)
			wx.EVT_CHECKBOX(self.panel, checkbox.GetId(), self.check_box_event)
			

			variable_description = wx.StaticText(self.panel, -1, label, style=0)
			self.grid_sizer.Add(variable_description)
		
		
		#This checks whether the base axis has been set earlier, if yes its len will be non -zero
		self.selected_checkboxes= [(checkbox.GetId(), checkbox.GetLabelText()) for checkbox in self.checkboxes if checkbox.GetValue()== True]


		#If the self.selected_checkboxes is non-zero, the statement below disables all the other checkboxes, To select new base axis
		#the checkbox before the porent base_axis has to be removed
		if bool(self.selected_checkboxes):
			[checkbox.Enable(False) for checkbox in self.checkboxes if checkbox.GetValue()== False]
		return

	def check_box_event(self, event):
		"""
		selected_checkboxes is the list of the checkboxes which are being clicked
		
		[checkbox.Enable(False) for checkbox in self.checkboxes if checkbox.GetValue()== False]
		Above statment disables all the checkboxes which are unclicked on the wx.dialog box

		"""
		self.selected_checkboxes= [(checkbox.GetId(), checkbox.GetLabelText()) for checkbox in self.checkboxes if checkbox.GetValue()== True]
		[checkbox.Enable(False) for checkbox in self.checkboxes if checkbox.GetValue()== False]
		if len(self.selected_checkboxes) == 0:
			[checkbox.Enable(True) for checkbox in self.checkboxes]
	
		try:
			self.checkbox = self.selected_checkboxes[0][1]
		except:
			self.checkbox = None
		return 

class ComparePlots(ChangeBaseAxis):

	def __init__(self, parent, base_axis, data):
		ChangeBaseAxis.__init__(self, parent, base_axis, data)
		self.text = "Select at most three variable to compare the plots on the common base axis"


	def populate_variables(self):
		"""
		Variables:
			variable_description:
				type(string) which was made by joining sepereted by comma, the first three values of the variables present
				in the data
		This also appends the checkboxes list, with each and every checkbox created corresponding to each and every variable present 
		in the data
		"""
		
		x = 20
		y = 20
		for integer, variable  in enumerate(self.data.columns):
			sample_variable_data = [str(i) for i in self.data[variable].values[0:3]]
			label = ",  ".join(sample_variable_data)

			checkbox= wx.CheckBox(self.panel, integer, variable, pos=(x+5, y))
			self.grid_sizer.Add(checkbox)
			if variable == self.base_axis:
				checkbox.SetValue(True)
			self.checkboxes.append(checkbox)
			wx.EVT_CHECKBOX(self.panel, checkbox.GetId(), self.check_box_event)
			

			variable_description = wx.StaticText(self.panel, -1, label, style=0)
			self.grid_sizer.Add(variable_description)
		return


	def check_box_event(self, event):
		"""
		selected_checkboxes is the list of the checkboxes which are being clicked
		
		[checkbox.Enable(False) for checkbox in self.checkboxes if checkbox.GetValue()== False]
		Above statment disables all the checkboxes which are unclicked on the wx.dialog box

		"""
		self.selected_checkboxes= [(checkbox.GetId(), checkbox.GetLabelText()) for checkbox in self.checkboxes if checkbox.GetValue()== True]
		if len(self.selected_checkboxes) == 4:
			[checkbox.Enable(False) for checkbox in self.checkboxes if checkbox.GetValue()== False]
	
		else:
			[checkbox.Enable(True) for checkbox in self.checkboxes]

		try:
			self.checkbox = self.selected_checkboxes
		except:
			self.checkbox = None

















