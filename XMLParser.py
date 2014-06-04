#!/usr/bin/env python
#-*- coding: utf-8 -*-

import wx
import xml.sax.handler
import sys

def xml_data(xml_file):
	file = open(xml_file,'r')
	data= file.read()
	file.close()
	return data.replace( "&", "&amp;" )




def createMenus(self, menuData, frame):

	class MenuBuilder(xml.sax.handler.ContentHandler):
		"""
		This class parses the xml present in the menudata
		class Variables:
			main_bar: type(string)
				This is the main bar onto which all the menu and submenus will be appended
			menu_names_list: type(list)
				This has elements which corresponds to the menuNames and the element has the form of tuple with
				three elements in it.the first element represent the wx.Menu object, the second element corresponds to
				name of the menu name, and third element represents the help text for this particular menu name

		How it Works:
			XML starts with the menubar, it tdoesnt have support for more toolbars, only one toolbar is possible
			on an encounter with menubar tag in the xml, main_bar variables is intialized with value as wx.MenuBar()

			on an encounter with menuName, which represents clickable text on the main toolbar, first element in the 
			menu_names_list is inserted, which is tuple with values mentiones above in this docstring.

			On an encounter with itemName, Its attributes been pulled and stored into class variables known as item_name, 
			help, type, handler.type represents whether its id is wx.NORMAL, wx.CHECK or wx.RADIO

			On an encounter with closing menuItem, the Variables which was intialised above is then appended to the last element
			in the menu_names_list as all the item names which was encountered after as encounter with opening meuItem belongs
			the the menuName

		"""
		
		def __init__(self):
			self.main_bar = None
			self.menu_names_list = list()
			self.item= str()
			self.type = str()

		def startElement(self, tag, attributes):
       	  	
			#This Method runs on every line present in the xml, here we intialise self.text to be empty string to make 
			#room for the new content present in the new child of xml
	 
			if tag == "menuItem":
				return 

			elif tag == "menubar":
				self.main_bar = wx.MenuBar()
 	     	     		return 

		    	elif tag == "menuName":
				self.menu_names_list.append((wx.Menu(), attributes.get("name"), attributes.get("help")))
				return 

			elif tag == "itemName":
				self.item_name = attributes.get("name")
				self.help = (attributes.get("help"), str())[attributes.get("help") == None]
				self.type = (attributes.get("kind"), str())[attributes.get("kind") == None]
				try:
					self.handler = getattr(frame, attributes.get("handler"))
				except Exception:
					raise KeyError, "The handler for  %s is not present in the base frame class"%self.item_name
				return 
	
			elif tag == "menu":
           			return 

	    		elif tag == "separator":
				pass
            
		    	else:
				raise ValueError, "Invalid menu component %s"%tag

		def endElement(self, tag):
	
			if tag == "menuItem":
				self.id= wx.NewId()
					
				if self.type == str() or self.type == "normal":
					self.item = self.menu_names_list[-1][0].Append(id=self.id, text=self.item_name, help=self.help)
       	         
				elif self.type == "check":
					self.item = self.menu_names_list[-1][0].AppendCheckItem(id=self.id, text=self.item_name, help=self.help)
       	         
				elif self.type == "radio":
					print "radio item appended"
					self.item = self.menu_names_list[-1][0].AppendRadioItem(id=self.id, text=self.item_name, help=self.help)
       	         
				else:
					raise ValueError, "Unknown item type %s" % self.type
				frame.Bind(wx.EVT_MENU, self.handler, id= self.id)
		    	
			elif tag == "menu":
			
				if len(self.menu_names_list) == 1:
					self.main_bar.Append(menu= self.menu_names_list[-1][0], title=self.menu_names_list[-1][1])

				else:
					self.menu_names_list[-2][0].AppendSubMenu(submenu= self.menu_names_list[-1][0], text=self.menu_names_list[-1][1], help= self.menu_names_list[-1][2])
				self.menu_names_list.pop(-1)


		    	elif tag == "itemName":
				pass

		    	elif tag =="separator":
				self.menu_names_list[0][0].AppendSeparator()
       	     
		    	elif tag =="menubar":
				try:
					font = wx.Font(2, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
					self.main_bar.SetFont(font)
				except Exception:
					pass
				frame.SetMenuBar(self.main_bar)
	
			elif tag == "menuName":
				pass	

			else:
				raise ValueError, "Invalid menu component %s" % name
	
	
	builder = MenuBuilder()
	xml.sax.parseString(menuData, builder)
