"""
The GUI calls the Engine multiple times 
to handle more than one MP3 at a time
"""

import wx

"""
If your build is failing here
then you didn't install the 
wxWidgets dependencies correctly

See the README for help
"""
def main():
    #Initialize wxWidgets
    wxApp = wx.App()
    topFrame = wx.Frame(None, -1, 'Lyrics Lasso')
    #topFrame.SetDimensions()
    topFrame.Show()
    wxApp.MainLoop()