#!/usr/bin/env python
#-*- coding: utf-8 -*-
import wx
import matplotlib
matplotlib.interactive(False)
import matplotlib.pylab as plt
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas                                                                      
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as NavigationToolbar 

class MatplotlibPanel(wx.Panel):
	def __init__(self, parent, id, data, minimum, maximum):
		self.id = id
		wx.Panel.__init__(self, parent, self.id, style=wx.SIMPLE_BORDER)
		self.data = data
		self.minimum = minimum
		self.maximum = maximum


		self.tooltip = wx.ToolTip(tip='Tip with a details of points')
		self.SetToolTip(self.tooltip)
		self.tooltip.Enable(True)
		self.tooltip.SetDelay(0)
		
		self.fig = plt.figure(self.id, figsize=(12, 6.5), dpi=100, facecolor="w", frameon=True)
		self.canvas = FigureCanvas(self, self.id, self.fig)
		self.toolbar = NavigationToolbar(self.canvas)
		mass_txt = wx.StaticText(self.toolbar, label='m/z', pos=(230, 7), size=(25, 17))
		mass_txt.SetBackgroundColour("light gray") 
		self.mass = wx.TextCtrl(self.toolbar, pos=(260,4), size=(50, 22), style=wx.TE_READONLY)
		self.toolbar.SetToolBitmapSize(wx.Size(24, 25))
		self.toolbar.SetMinSize((1500, 40))
		self.toolbar.Realize()
		self.toolbar.Update()

		
		self.fig.canvas.mpl_connect('button_press_event', self.onclick)
		self.fig.canvas.mpl_connect('pick_event', self.on_pick)
		self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
		self.fig.canvas.mpl_connect('key_press_event', self.on_key)



		self.SetAutoLayout(True)	
		self.SetBackgroundColour('midnight blue')
		# Now put all into a sizer
		sizer = wx.BoxSizer(wx.VERTICAL)
		# This way of adding to sizer allows resizing
		sizer.Add(self.canvas, 5, wx.LEFT|wx.TOP|wx.GROW)
		# Best to allow the toolbar to resize!
		sizer.Add(self.toolbar, 0, wx.GROW)
		self.SetSizer(sizer)
		self.Fit()
		print "matplotlib has been changed"
		print "matplotlib panel class with id %s"%self.id

	def onclick(self, event):
		print "generated from onclick event This is X=%s and Y=%s"%(event.xdata, event.ydata)
		return


	def on_pick(self, event):
		print "Onpick called"
		x_label = self.fig.axes[0].get_xlabel()
		y_label = self.fig.axes[0].get_ylabel()
		xdata, ydata = event.artist._offsets[:,0], event.artist._offsets[:,1]
		self.x , self.y = np.take(xdata, event.ind[0]), np.take(ydata, event.ind[0])
		
		top = tip='%s: %.2f\n%s: %.2f'%(x_label, self.x, y_label, self.y)
		self.tooltip.SetTip(tip) 
		self.tooltip.Enable(True)
		return

	def on_motion(self, evt):
		if evt.inaxes:
			xpos = evt.xdata
			self.mass.SetValue(' %0.1f' % (xpos))

	def on_key(self, event):
		if 'escape' == event.key:
			self._is_pick_started = False
			self._picked_indices = None
