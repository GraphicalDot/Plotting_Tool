#!/usr/bin/env python
#-*- coding:utf-8 -*-
import numpy
import matplotlib.pylab as plt

"""
This Python file will have all the functions related to one dimensional plotting in the matplotlib

"""
def remove_axis_spines():
	for direction in ["left", "right", "top", "bottom"]:
		ax.spines[direction].set_color("none")
	return

def adjust_plot_dimensions():
	plt.subplots_adjust(left=0.04, right=0.94, top=0.95, bottom=0.07)
	return


#def one_d_line_plot(base_axis, data, selected_checkboxes, panel, minimum, maximum):
def one_d_line_plot(*args):
   	"""
	base_axis, data, selected_checkboxes, panel, minimum, maximum
	"""
	dictionary = args[0]
	base_axis_data = dictionary["base_axis_data"]
	data = dictionary["data"]
	selected_checkboxes = dictionary["selected_checkboxes"]
	panel = dictionary["panel"]
	maximum = dictionary["maximum"]
	minimum = dictionary["minimum"]
	size = dictionary["minimum"]
	minimum = dictionary["minimum"]

	panel.canvas.figure.clf()
	print "from one D plots %s"%panel.GetId()
	if len(base_axis_data) != 0:
		try:
			
			y_ticks = list(set(data))
			panel.canvas.figure.clf()
			ax = panel.canvas.figure.add_subplot(111)
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			ax.plot(base_axis_data, data, s=1, c="b")
			panel.canvas.draw()
		except:
			panel.canvas.figure.clf()
			ax = panel.canvas.figure.add_subplot(111)
	
	
			y_ticks = list(set(data))
			y_data = [y_ticks.index(element) for element in data]
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			ax.set_yticks(range(len(y_ticks)))
			ax.set_yticklabels(y_ticks)
			
			x_ticks = list(set(base_axis_data))
			x_data = [element for element in base_axis_data]
			
			plt.plot(x_data, y_data, s=1, c="b")
			panel.canvas.draw()

	else:
	   
		try:
			x_ticks = range(minimum, maximum)
			y_ticks = list(set(data))
			ax = panel.canvas.figure.add_subplot(111)
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			ax.plot(range(0, data.size), data)
			panel.canvas.draw()
	
		except:
			ax = panel.canvas.figure.add_subplot(111)
			
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			y_ticks = list(set(data))
			ax.set_yticks(range(len(y_ticks)))
			ax.set_yticklabels(y_ticks)
			
			y_data= [y_ticks.index(element) for element in data]
			plt.plot(range(0, data.size), y_data)
			panel.canvas.draw()
		
	return


def OneD_Line_Same_XAxis(x1, x2, selected_checkboxes, panel):
                panel.canvas.figure.clf()
		plt.plot(range(0, x1.size), x1, color="red")
		plt.plot(range(0, x2.size), x2, color="blue")
		
		panel.canvas.draw()


def OneD_Compare_Plots(panel, variable_list, base_axis, data, minimum, maximum):
	data = data[minimum: maximum]
	##TODO: Not been implemented yet
	panel.canvas.figure.clf()
	axes = plt.subplots(nrows=2, ncols=2)
	variable_names = [variable for (id, variable) in variable_list]
	print variable_names

	print data[variable_names[0]]
	data[variable_names[0]].values.plot(ax=axes[0,0]); axes[0,0].set_title(variable_names[0])
	data[variable_names[1].values].plot(ax=axes[0,1]); axes[0,1].set_title(variable_names[1])
	data[variable_names[2].values].plot(ax=axes[1,0]); axes[1,0].set_title(variable_names[2])
	data[variable_names[3].values].plot(ax=axes[1,1]); axes[1,1].set_title(variable_names[3])
	panel.canvas.draw()
	return







