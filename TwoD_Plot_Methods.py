#!/usr/bin/env python
#-*- coding: utf-8 -*-

import matplotlib.pylab as plt
import numpy as np

def remove_axis_spines(ax):
	for direction in ["left", "right", "top", "bottom"]:
		ax.spines[direction].set_color("none")
	return

def adjust_plot_dimensions():
	plt.subplots_adjust(left=0.04, right=0.94, top=0.95, bottom=0.07)
	return

def TwoD_Scatter(x, y, selected_checkboxes,  panel, s=None, c=None):
	"""
	This method is used to plot a two dimensional graphs on the basis of the selected checkboxes from the pyscrolledwindow
	s is the size of the points being drawn
	c is the color of the points being drawn
	"""
	if c is None:
		c = "b"
	if s is None:
		s= 10
	
	plt.xlabel(selected_checkboxes[0][1])
	plt.ylabel(selected_checkboxes[1][1])
	try:

		panel.canvas.figure.clf()
		plt.xlim(np.min(x), np.max(x))
		plt.ylim(np.min(y), np.max(y))
		plt.grid(True)
		scatter = plt.scatter(x, y,marker="o", s=s, c=plt.randn(len(x)), picker= True)
		plt.subplots_adjust(left=0.05, right=0.94, top=0.95, bottom=0.09)
	except:
		try:
			panel.canvas.figure.clf()
			ax = panel.canvas.figure.add_subplot(111)  
			y_ticks = list(set(y))
			ax.set_yticks(range(len(y_ticks)))
			ax.set_yticklabels(y_ticks)
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			y_data= [y_ticks.index(element) for element in y]
			plt.scatter(x, y_data)
		except:
			panel.canvas.figure.clf()
			ax = panel.canvas.figure.add_subplot(111)  
			y_ticks = list(set(y))
			ax.set_yticks(range(len(y_ticks)))
			ax.set_yticklabels(y_ticks)
			for direction in ["left", "right", "top", "bottom"]:
				ax.spines[direction].set_color("none")
			y_data= [y_ticks.index(element) for element in y]
			x_ticks = list(set(x))
			ax.set_xticks(range(len(x_ticks)))
			ax.set_xticklabels(x_ticks)
			x_data= [x_ticks.index(element) for element in x]
			plt.scatter(x_data, y_data)
		
	panel.canvas.draw()
	return

def TwoD_Hexbin(x,  panel):
#	plt.xlim(np.min(x), np.max(x))
#	plt.ylim(np.min(y), np.max(y))
#	plt.grid(True)
#	plt.hexbin(x, y, bins='log', cmap=plt.cm.YlOrRd_r)
	plt.hist(x)
	plt.subplots_adjust(left=0.03, right=0.98, top=0.98, bottom=0.07)
	panel.canvas.draw()
	return

