# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItem_open = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItem_open )

		self.m_menuItem_save = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItem_save )

		self.m_menubar.Append( self.m_menuFile, u"File" )

		self.m_menuEdit = wx.Menu()
		self.m_menuItem_setAutoSaveTo10s = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Set auto save to 10s", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItem_setAutoSaveTo10s )

		self.m_menuItem_setAutoSaveTo1m = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Set auto save to 1m", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItem_setAutoSaveTo1m )

		self.m_menuItem_setAutoSaveTo1h = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Set auto save to 1h", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItem_setAutoSaveTo1h )

		self.m_menuItem_setNotepadPath = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Set notepad++ path", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItem_setNotepadPath )

		self.m_menubar.Append( self.m_menuEdit, u"Edit" )

		self.SetMenuBar( self.m_menubar )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_textCtrl, 1, wx.ALL, 5 )

		self.m_button_update = wx.Button( self, wx.ID_ANY, u"update", wx.DefaultPosition, wx.Size( 60,25 ), 0 )
		bSizer1.Add( self.m_button_update, 0, wx.ALL, 5 )

		self.m_button_copy = wx.Button( self, wx.ID_ANY, u"copy", wx.DefaultPosition, wx.Size( 60,25 ), 0 )
		bSizer1.Add( self.m_button_copy, 0, wx.ALL, 5 )


		bSizer.Add( bSizer1, 0, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer2_1 = wx.BoxSizer( wx.HORIZONTAL )

		# self.m_button_addNewLine = wx.Button( self, wx.ID_ANY, u"Add new line", wx.DefaultPosition, wx.DefaultSize, 0 )
		# bSizer2_1.Add( self.m_button_addNewLine, 0, wx.ALL, 5 )

		self.m_button_setAllTo0 = wx.Button( self, wx.ID_ANY, u"Set all TOGGLE", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2_1.Add( self.m_button_setAllTo0, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer2_1, 0, wx.EXPAND, 5 )

		bSizer2_2 = wx.BoxSizer( wx.VERTICAL )

		self.m_grid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid.CreateGrid( 200, 5 )
		self.m_grid.EnableEditing( True )
		self.m_grid.EnableGridLines( True )
		self.m_grid.EnableDragGridSize( False )
		self.m_grid.SetMargins( 0, 0 )

		# Columns
		self.m_grid.SetColSize( 0, 72 )
		self.m_grid.SetColSize( 1, 336 )
		self.m_grid.SetColSize( 2, 274 )
		self.m_grid.SetColSize( 3, 145 )
		self.m_grid.SetColSize( 4, 139 )
		self.m_grid.EnableDragColMove( False )
		self.m_grid.EnableDragColSize( True )
		self.m_grid.SetColLabelSize( 30 )
		self.m_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid.EnableDragRowSize( True )
		self.m_grid.SetRowLabelSize( 80 )
		self.m_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer2_2.Add( self.m_grid, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer2_2, 1, wx.EXPAND, 5 )


		bSizer.Add( bSizer2, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


