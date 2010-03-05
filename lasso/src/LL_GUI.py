"""
The GUI calls the Engine multiple times 
to handle more than one MP3 at a time
"""

import wx
import os
import LL_dev
_dP = LL_dev._dP
#os.getcwd() = current dir
#os.chdir() = change cwd
#os.listdir = all files in a dir

DEV_MODE = 1

"""
If your build is failing here
then you didn't install the 
wxWidgets dependencies correctly

See the README for help
"""
def main():
    #Initialize wxWidgets
    
    #This class handles the bulk of what is within the main wxApp
    #You can ignore any "Undefined variable from import: [Component Name]" 
    # notices, unless your build actually fails
    class wxMain(wx.Frame):
        def __init__(self,parent,title):
            wx.Frame.__init__(self,parent,title=title,size=(200,100))
            
    #Setup an application to store frame
    #BUT DO NOT REDIRECT I/O TO THE GUI!!! (False)
    wxApp = wx.App(False)
    topFrame = wx.Frame(None, -1, 'Lyrics Lasso')
    #topFrame.SetDimensions()
    topFrame.Show()
    wxApp.MainLoop()
