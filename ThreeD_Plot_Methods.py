#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D 

def ThreeD_Scatter(x, y, z, selected_checkboxes, panel, auto_rotate, axis_3d=True):

	ax = Axes3D(panel.fig)
	ax.grid(False)
	ax.set_xlabel(selected_checkboxes[0][1])
	ax.set_ylabel(selected_checkboxes[1][1])
	ax.set_zlabel(selected_checkboxes[2][1])
	ax.set_xlim(np.min(x), np.max(x))
	ax.set_ylim(np.min(y), np.max(y))
	ax.set_ylim(np.min(z), np.max(z))

	if not axis_3d:
		ax._axis3don = False
	
	ax.scatter3D(x, y, z,  s=15, c= plt.randn(len(x)))
#	ax.plot_surface(x, y, z,  s=1)
#	def onpick(event):
#		ind = event.ind[0]
#		x, y, z = event.artist._offsets3d
#		print x[ind], y[ind], z[ind]
#	panel.fig.canvas.mpl_connect('pick_event', onpick)	


	
	if auto_rotate:
		for i in xrange(0,360,5):
			ax._axis3don = axis_3d
			ax.view_init(elev=10. +i, azim=i)
			panel.canvas.draw()
		return 
	panel.canvas.draw()
	return

