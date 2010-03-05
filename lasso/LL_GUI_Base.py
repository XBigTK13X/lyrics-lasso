#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Thu Mar 04 21:03:48 2010

import wx

# begin wxGlade: extracode
# end wxGlade



class wxFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.frame_2_menubar = wx.MenuBar()
        self.file = wx.Menu()
        self.chdir = wx.MenuItem(self.file, chdir, "Change Directory", "", wx.ITEM_NORMAL)
        self.file.AppendItem(self.chdir)
        self.frame_2_menubar.Append(self.file, "File")
        self.SetMenuBar(self.frame_2_menubar)
        # Menu Bar end
        self.frame_2_statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.frame_2_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_2_toolbar)
        self.frame_2_toolbar.AddLabelTool(wx.NewId(), "chdir", wx.Bitmap("C:\\Users\\KRETST\\Documents\\workspace\\Lyrics_Lasso\\src\\GFX\\chdir.bmp", wx.BITMAP_TYPE_ANY), wx.Bitmap("C:\\Users\\KRETST\\Documents\\workspace\\Lyrics_Lasso\\src\\GFX\\chdir.bmp", wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "", "")
        # Tool Bar end

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxFrame.__set_properties
        self.SetTitle("frame_2")
        self.SetSize((600, 555))
        self.SetFocus()
        self.frame_2_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_2_statusbar_fields = ["frame_2_statusbar"]
        for i in range(len(frame_2_statusbar_fields)):
            self.frame_2_statusbar.SetStatusText(frame_2_statusbar_fields[i], i)
        self.frame_2_toolbar.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class wxFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = (None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()