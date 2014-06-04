#!/usr/bin/env python
#-*- coding: utf-8 -*-
from pandas.tools.plotting import parallel_coordinates
from pandas.tools.plotting import radviz
from pandas.tools.plotting import andrews_curves

def prepare_panel():
	return 

def Evt_Multi_D_Parellel_Plot(self, event):
	page = self.New_Tab.GetSelection()  
	panel = self.New_Tab.GetPage(page)
	self.selected_checkbox()
	panel.canvas.figure.clf()
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
