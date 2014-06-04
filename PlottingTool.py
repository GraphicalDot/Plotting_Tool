#!/usr/bin/env python
#-*- coding:utf-8 -*-
from numpy import arange, sin, pi
import subprocess
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pylab as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as NavigationToolbar
import os
import wx
import re
import sys
import time
import itertools
import hashlib
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
import matplotlib.animation as animation
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
#from Animation import AnimatedScatter
import pandas
import multiprocessing
from matplotlib_panel import MatplotlibPanel
from OneD_Plot_Methods import one_d_line_plot, OneD_Line_Same_XAxis, OneD_Compare_Plots
from TwoD_Plot_Methods import TwoD_Scatter, TwoD_Hexbin
from ThreeD_Plot_Methods import ThreeD_Scatter
import XMLParser
from Helpers import DataSize, ChangeBaseAxis, ComparePlots
import wx.lib.agw.flatnotebook as fnb
from wx.lib.colourdb import getColourList
import subprocess
import matplotlib
file_matplotlibrc = matplotlib.matplotlib_fname()


"""
Uncomment this line if you want to replace your matplotlib settings file with the one, available in this repository
subprocess.call["cp", matplotlibrc, file_matplotlibrc]
"""

#This list has all the colors available in wx python
colors = [color for color in getColourList()]



class RedirectText(object):
	def __init__(self, aWxTextCtrl):
		self.out = aWxTextCtrl
			     
	def write(self,string):
		self.out.WriteText(string)


class CanvasPanel(wx.Frame):
	def __init__(self, data):

		"""
		Class Variables:
			self.data: data which is to be plotted.

			self.x_data: slice of the self.data alongthe x-axis
			self.y_data: slice of the self.data alongthe y-axis
			self.z_data: slice of the self.data alongthe z-axis.

			self.minimum: Intialised with the value 0, Default slicing for the data
			self.maximum: Intialised with the value 10000, Default slicing of the data, Both these class variable implies that the 
					Intial plot data will be plotted from data[self.minimum: self.maximum]

			Their values can be changed from the "Go Plot!!" button present at the end of the Frame.

			self.log_panel: wx.Panel which will have the standard input and out bound to it.
			self.New_Tab: wx.Notebook which is opened as a new tab whenever the new tab option is clicked from the file menu.

		"""
		
		self.selected_checkboxes = list()
		self.axis_3d = True
		self.tab_count = 0
		self.minimum = 0
		self.maximum = 1000
		self.data = data
		self.x_data= None
		self.y_data= None
		self.z_data= None
		self.base_axis = None
		
		wx.Frame.__init__(self, None, -1, size=(800,600), pos=((wx.DisplaySize()[0])/2,(wx.DisplaySize()[1])/2), style=wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		self.Button_vbox= wx.BoxSizer(wx.VERTICAL)

		#Splitter window
		self.window= wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER, size=(800,600))	
		
		
		#Two panels
		self.left_panel = wx.Panel(self.window, wx.ID_ANY)
		self.right_panel = wx.Panel(self.window, wx.ID_ANY)
		



		#Notebook on which the matplotlib panel will be inserted
		self.New_Tab = fnb.FlatNotebook(self.right_panel, style=fnb.FNB_TABS_BORDER_SIMPLE|fnb.FNB_VC71)


		font = wx.Font(6, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
		font_bottom = wx.Font(7, wx.FONTFAMILY_TELETYPE, wx.FONTFAMILY_DECORATIVE, wx.FONTWEIGHT_BOLD, True, u'Comic Sans MS')

		self.matplotlib_panel= MatplotlibPanel(self.New_Tab, self.tab_count, self.data, self.minimum, self.maximum)
		self.New_Tab.AddPage(self.matplotlib_panel, "Tab %s"%self.tab_count)
		self.tab_count += 1

		#This panel will have all the varibales present in the data file
		self.wxpanel= wx.PyScrolledWindow(self.left_panel, -1,)
		self.wxpanel.SetFont(font_bottom)
		self.wxpanel.SetBackgroundColour("DARKCYAN")
		self.log_window = wx.TextCtrl(self.left_panel, wx.ID_ANY, size=(300, 150), style = wx.TE_MULTILINE|wx.VSCROLL|wx.TE_BESTWRAP| wx.TE_WORDWRAP)
		self.log_window.SetFont(font)

		#This method populates the variable spresent in the file into the scrolled window
		self.checkbox_list = list()
		self.populate_variables(self.data, self.wxpanel, self.checkbox_list)


		self.vbox_left = wx.BoxSizer(wx.VERTICAL)
		self.vbox_left.Add(self.log_window, 0, wx.EXPAND| wx.ALL, 2)
		self.vbox_left.Add(self.wxpanel, 1, wx.EXPAND| wx.ALL, 2)
		self.left_panel.SetSizer(self.vbox_left)
		
		self.vbox_right = wx.BoxSizer(wx.VERTICAL)
		self.vbox_right.Add(self.New_Tab, 20, wx.EXPAND| wx.ALL, 1)
		self.right_panel.SetSizer(self.vbox_right)
		
		
		#This part generates the menu from the menu.xml present in the same directory
		menudata = XMLParser.xml_data("menu.xml")
		XMLParser.createMenus(self, menudata, self)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.window.SplitVertically(self.left_panel, self.right_panel)
		sizer.Add(self.window, 1, wx.EXPAND, 0)
		self.SetSizer(sizer)
		sizer.Fit(self)
		
		#This part redirects the standard output and standard input on the console embedded in the wx.Frame
		redir = RedirectText(self.log_window)
		sys.stdout = redir
		sys.stderr = redir
#		self.SetSizer(self.hbox)
		self.SetBackgroundColour("light blue")
		self.statusbar = self.CreateStatusBar()
		self.Centre()
		self.Show()

	def remove_axis_spines(self, ax):
		for direction in ["left", "right", "top", "bottom"]:
			ax.spines[direction].set_color("none")
		return

	def adjust_plot_dimensions(self):
		plt.subplots_adjust(left=0.04, right=0.94, top=0.95, bottom=0.07)

		return
	

	def Evt_Tab_Changing(self, event):
		"""
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.New_Tab.GetSelection()
		print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
		"""
		event.Skip()
		

	def Evt_Tab_Changed(self, event):
		page = self.New_Tab.GetPageText(event.GetSelection())
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.New_Tab.GetSelection()
		event.Skip()



	def populate_variables(self, data, panel, checkboxes):
		"""
		This method generates the variables present in the data and emebed them into the wx.Panel
		"""
		x = 5       
		y = 20
		for integer, variable  in enumerate(data.columns):
			checkbox= wx.CheckBox(panel, integer, variable, pos=(x+5, y))
			w, h = checkbox.GetSize()
			checkbox.SetValue(False)
			checkboxes.append(checkbox)
			wx.EVT_CHECKBOX(panel, checkbox.GetId(), self.Evt_Checkbox)
			dy = h + 1 
			y += dy

		panel.SetScrollbars(1, dy,  1, y/dy+1)
		panel.SetScrollRate(1, 1 )			
		return 	

	def Evt_Scatter_Plot(self, event):
		print "Event scatter plot has been clicked"
		return 

	def Evt_Line_Plot(self, event):
		print "Event line plot has been clicked"
		return 



	def Evt_Change_Base_Axis(self, event):
		data_dialog = ChangeBaseAxis(self, self.base_axis, self.data)
		if data_dialog.ShowModal() == wx.ID_OK:
			if data_dialog.checkbox:
				self.base_axis = data_dialog.checkbox
			data_dialog.Destroy()			
		return


	def Evt_Auto_Rotate_ThreeD_Plot(self, event):
		
		if event.IsChecked():
			ThreeD_Scatter(self.x_data[self.minimum: self.maximum], self.y_data[self.minimum: self.maximum], self.z_data[self.minimum: 
			self.maximum], self.selected_checkboxes, self.matplotlib_panel, auto_rotate= True, axis_3d= self.axis_3d)
		return 


	def Evt_Multiple_Plots(self, event):
		self.selected_checkboxes
		panel.canvas.figure.clf()
		with pd.plot_params.use('x_compat', True):
			df.A.plot(color='r')
			df.B.plot(color='g')
			df.C.plot(color='b')

		panel.canvas.draw()


	def Evt_Same_XAxis(self, evt):
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		
		NUM_COLORS = 20
		panel.canvas.figure.clf()
		cm = plt.get_cmap('gist_rainbow')
		fig = panel.fig
		ax = fig.add_subplot(111)
		ax.set_color_cycle([cm(3.*i/NUM_COLORS) for i in range(NUM_COLORS)])
	
		self.remove_axis_spines(ax)
		self.adjust_plot_dimensions()

		for i in range(len(self.selected_checkboxes)):
			color = cm(3.*i/NUM_COLORS)
			ax.plot(self.data[self.selected_checkboxes[i][1]].values[self.minimum: self.maximum], label=self.selected_checkboxes[i][1])
			print "ax plotted %s"%i
		
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
		panel.canvas.draw()
		return 

	def Evt_Multi_D_Parellel_Plot(self, event):
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		panel.canvas.figure.clf()
		from pandas.tools.plotting import parallel_coordinates
		data_list = list()
		for variable in self.selected_checkboxes:
			data_list.append(variable[1])

		data_list.append("customer_number")
		data = self.data[data_list][self.minimum: self.maximum]

		ax = parallel_coordinates(data, "customer_number")
		for direction in ["left", "right", "top", "bottom"]:
			ax.spines[direction].set_color("none")
		panel.canvas.draw()
		return

	def Evt_Multi_D_Radviz_Plot(self, event):
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		panel.canvas.figure.clf()
		from pandas.tools.plotting import radviz
		data_list = list()
		for variable in self.selected_checkboxes:
			data_list.append(variable[1])

		data_list.append("customer_number")
		data = self.data[data_list][self.minimum: self.maximum]

		radviz(data, "customer_number")
		panel.canvas.draw()
		return


	def Evt_Multi_D_Andrew_Plot(self, event):
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		panel.canvas.figure.clf()
		from pandas.tools.plotting import andrews_curves
		data_list = list()
		for variable in self.selected_checkboxes:
			data_list.append(variable[1])

		data_list.append("customer_number")
		data = self.data[data_list][self.minimum: self.maximum]

		ax= andrews_curves(data, "customer_number")
		for direction in ["left", "right", "top", "bottom"]:
			ax.spines[direction].set_color("none")
		panel.canvas.draw()
		return

	def Evt_Multi_D_Radar_Plot(self, event):
		raise KeyError("This Plot has not been implemented yet")

		return


	def Evt_Bootstrap_Plot(self, event):
		from pandas.tools.plotting import bootstrap_plot
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		panel.canvas.figure.clf()

		if len(self.selected_checkboxes) == 1:
			bootstrap_plot(self.data[self.selected_checkboxes[0][1]][self.minimum: self.maximum], fig= panel.canvas.figure)
			panel.canvas.draw()

		else:
			raise KeyError("Bootstrap plot can only be drawn with One variable")

		return

	def Evt_Data_Size(self, event):
		"""
		This event is binded to "Data Size" button present in the menubar, It deals with the change in data size, 
		It sets two class variables according to the values enetered in the dialog box.
		self.maximum
		self.minimum

		After setting these two values all the plots that is being drawn after setting these two values, will have only points
		specified by self.maximum and self.minimum


		"""
		data_dialog = DataSize(self, -1, self.minimum, self.maximum, 'combobox.py')
		if data_dialog.ShowModal() == wx.ID_OK:
			self.minimum = int(data_dialog.min_value_text.Value)
			self.maximum =  int(data_dialog.max_value_text.Value)
		
			
			#Reintialising the matplotlib_panel, as the values for maximum and minimum has been changed
			self.CheckBox_plot()
			data_dialog.Destroy()			
		return


	

	def Evt_Compare_Plots(self, event): #E represents Event, B = bar, PD= pandas
		data_dialog = ComparePlots(self, self.base_axis, self.data)
		if data_dialog.ShowModal() == wx.ID_OK:
			if data_dialog.checkbox:
					OneD_Compare_Plots(self.matplotlib_panel, data_dialog.checkbox, self.base_axis, self.data, self.minimum, self.maximum)
			data_dialog.Destroy()			
		return


	def Evt_Animate(self, event, number=None):
		if number is None:
			number= 1000
		
		self.matplotlib_panel.canvas.figure.clf()
		plt.xlim(np.min(self.x_data), np.max(self.x_data))
		plt.ylim(np.min(self.y_data), np.max(self.y_data))
		data_stream= (element for element in zip(self.x_data, self.y_data))
		
		def take(n ,iterable):
			return list(itertools.islice(iterable, n))


		def plotting():
			for i in range(self.x_data.shape[0]):
				data = np.array(take(number, data_stream))
				plt.scatter(data[:, 0], data[:, 1],  s=3,)
				self.matplotlib_panel.canvas.draw()
		
		plotting()	
		return 

	def Evt_Break_Plot(self, event):
		"""
		This events deals with the Option &Break Plot, It simulatnaeouly plots the variables thats been checked 
		"""
		
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		panel.canvas.figure.clf()
		for i in range(len(self.selected_checkboxes)):
			ax = panel.canvas.figure.add_subplot(len(self.selected_checkboxes), 1, i + 1)
			ax.set_title("Plot #%s"%self.selected_checkboxes[i][1])
			ax.plot(self.data[self.selected_checkboxes[i][1]].values[self.minimum: self.maximum])
		self.matplotlib_panel.canvas.draw()
		return 


	def Evt_Hexbin(self, event):
		self.matplotlib_panel.canvas.figure.clf()
		TwoD_Hexbin(self.x_data[self.minimum: self.maximum], self.matplotlib_panel)
		return 


	def Evt_Checkbox(self, event):
		"""
		This event is instantiated whenever there is a change in the number of checkbox being clicked present on the left
		hand side of the window.
		This in turns calls CheckBox_plot to take action based on the checkboxes been clicked.

		"""
		self.CheckBox_plot()
		return 


	def selected_checkbox(self):
#		checkboxes= [checkbox.GetLabelText() for checkbox in self.checkbox_list if checkbox.GetValue()== True]
		self.selected_checkboxes= [(checkbox.GetId(), checkbox.GetLabelText()) for checkbox in self.checkbox_list if checkbox.GetValue()== True]
		return


	def CheckBox_plot(self):
		"""
		variable = data[column name which is being selected is in the form of tuple(id, label)]
		the variable is in the form of "(index, values) in enumerate()"
		To get the values we do variable.values
		To get the values according to self.maximum and self.minimum we do variable.values[self.minimum: self.maximum]
		Which gives the expression as 
		x = lambda: self.data[self.selected_checkboxes[0][1]].values[self.minimum: self.maximum]

		"""
		page = self.New_Tab.GetSelection()  
		panel = self.New_Tab.GetPage(page)
		self.selected_checkbox()
		
		x = lambda: self.data[self.selected_checkboxes[0][1]].values[self.minimum: self.maximum]
		y = lambda: self.data[self.selected_checkboxes[1][1]].values[self.minimum: self.maximum]
		z = lambda: self.data[self.selected_checkboxes[2][1]].values[self.minimum: self.maximum]


		if len(self.selected_checkboxes)== 2:
			[checkbox.Enable(True) for checkbox in self.checkbox_list if checkbox.GetValue()== False]
			self.x_data, self.y_data= x(), y()
			TwoD_Scatter(x(), y(), self.selected_checkboxes, panel)
		

		elif len(self.selected_checkboxes)== 3:
			self.x_data, self.y_data, self.z_data = x(), y(), z()
			ThreeD_Scatter(x(), y(), z(), self.selected_checkboxes, panel, auto_rotate= False, axis_3d= self.axis_3d)
			

		elif len(self.selected_checkboxes)== 1: 
			self.x_data= x()
			if self.base_axis:
				base_axis_data = self.data[self.base_axis].values[self.minimum: self.maximum]
			else:
				base_axis_data = list()

			data = {"base_axis_data": base_axis_data,
				"data": x(),
				"selected_checkboxes": self.selected_checkboxes,
				"panel": panel,
				"minimum": self.minimum,
				"maximum": self.maximum,
				"size": 2,
				"color": "blue",
				}

			one_d_line_plot(data)

		else:
			panel.canvas.figure.clf()
		return	

	def Evt_Remove_Axis_3d_Plots(self, event):
		"""
		This is the event which is used to remove axes lines and axis labels from the 3d plots.
		it When clicked sets off the self.axis_3d = False

		"""
		self.axis_3d = (True, False)[event.IsChecked() == True]
		print "This is the self.axis_3d value %s"%self.axis_3d
		return




	def Evt_Open_File(self, event):
		dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			mypath = os.path.basename(path)
			self.SetStatusText("You selected: %s" % mypath)
		dlg.Destroy()



							

	def Evt_Dot_Size(self, event):
		print "THe menu bar item to change the dotsize has been clicked"
	
	def Evt_Dot_Color(self, event):
		print "THe menu bar item to change the dotsize has been clicked"
	
	
	def Evt_New_Tab(self, event):
		"""
		This is the event that binds to the "New Tab" button present in the menubar, under the file menu option.
		This deals with the process of creating a new matplotlib panel inserted in the fnb.FLAT_NOTEBOOK page.
		After adding a new tab on the wx.Panel it increments self.tab_count by a factor of 1
		"""
		
		print "Evt_New_Tab the id of the new panel on new tab = %s"%self.New_Tab.GetPageCount()
		self.matplotlib_panel= MatplotlibPanel(self.New_Tab, self.tab_count, self.data, self.minimum, self.maximum)
		self.New_Tab.AddPage(self.matplotlib_panel, "Tab %s"%self.tab_count)
		self.tab_count += 1
		return



	def Evt_Close(self, e):
		dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = dial.ShowModal()
			        
		if ret == wx.ID_YES:
			with wx.BusyInfo('Please wait...'):
				self.Destroy()
		else:
			e.Veto()

	def Evt_Save(self, event):
		file_choices = "PNG (*.png)|*.png"
		dlg = wx.FileDialog(self, message="Save plot as...", defaultDir=os.getcwd(), defaultFile="plot.png", 
				wildcard=file_choices, style=wx.SAVE)
			         
		if dlg.ShowModal() == wx.ID_OK: 
			path = dlg.GetPath()
			self.canvas.print_figure(path, dpi=150)
			self.flash_status_message("Saved to %s" % path)
									         
	
	def flash_status_message(self, msg, flash_len_ms=1500):
		self.statusbar.SetStatusText(msg)
		self.timeroff = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_flash_status_off, self.timeroff)
		self.timeroff.Start(flash_len_ms, oneShot=True)
					    
	def on_flash_status_off(self, event):
		self.statusbar.SetStatusText('')

		return


class NewTab(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		t = wx.StaticText(self, -1, "This is a New Tab", (60,60))


def run_app(FILE):
	try:
		data = pandas.read_csv(FILE)
	except IOError:
		print "The file name which is written in this executable is not valid\n\n"
		FILE = raw_input("Please Enter the path of the file to be opened  ")
		if not os.path.exists(FILE):
			print "Go to Hell, You enetered PATHNAME which doesnt exists, try again"
			return 
		data = pandas.read_csv(FILE)
	app = wx.PySimpleApp()
	app.frame = CanvasPanel(data)
	app.frame.Show(True)
	app.frame.Center()
	app.MainLoop()



if __name__ == "__main__":

	try:
		import xlrd
	except ImportError:
		print  "No Module name xlrd"
		pass
	
	FILE = "/home/k/Desktop/Raj_Retail/new_customers.csv"

	FILE_EXTENSION = FILE.split(".")

	if FILE_EXTENSION[-1] == "csv":
		run_app(FILE)
	
	elif FILE_EXTENSION[-1] == "xlsx" or FILE_EXTENSION[-1] == "xls":
		file = xlrd.open_workbook(FILE)
		sheet = file.sheet_by_name("SHEET1")
		subprocess.call(["touch", "myfile.csv"])
		
		csv_file = open("myfile.csv", "wb")
		writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

		for rownum in xrange(sheet.nrows):
			writer.writerow(sheet.row_values(rownum))
			csv_file.close()

		csv_file.close()
		FILE = "/home/k/Desktop/myfile.csv"
		run_app(FILE)

	else:
		raise ValueError, "The Formaat of the data file is not supported yet"
