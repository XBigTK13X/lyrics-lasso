"""
The GUI calls the Engine multiple times 
to handle more than one MP3 at a time
"""

import os
import LL_dev
import LL_Engine
from wx._core import EVT_MENU
_dP = LL_dev._dP
#os.getcwd() = current dir
#os.chdir() = change cwd
#os.listdir = all files in a dir

"""
If your build is failing here
then you didn't install the 
wx.Widgets dependencies correctly

See the README for help
"""
import wx

#These call create Stock Item IDs. These are useful in creating
#items for menus later on
ID_ABOUT = wx.NewId()
ID_EXIT  = wx.NewId()
ID_OPEN = wx.NewId()
ID_TIMER = wx.NewId()

#These global variables will be used to track the 
#current working directory and current working file
currentFileName = ""
ENGINE = LL_Engine.Engine()

#This is the bulk of the GUI's programming
#This will be the class used to generate 
#The application's main frame
class mainFrame(wx.Frame):
    #Standard class requirement
    #This function is what is called when
    #creating a new instance of a class
    def __init__(self, parent, ID, title):
        #This creates a new frame. Frames are what hold everything
        #you see in an application's window
        wx.Frame.__init__(self, parent, ID, title,wx.DefaultPosition, wx.Size(600, 450))
        #This generates a status bar (The thing in the window
        #that displays the current working directory)
        self.CreateStatusBar()
        self.SetStatusText("CWD: "+os.getcwd())
        #Menus are what contain various actions at the top
        #of a window. In Eclipse, "File", "Edit", etc. are each 
        #a separate menu entity
        fileMenu = wx.Menu()
        fileMenu.Append(ID_OPEN, "&Open")
        fileMenu.Append(ID_EXIT, "E&xit")
        #Another Menu
        helpMenu = wx.Menu()
        helpMenu.Append(ID_ABOUT, "&About")
        #The Menu Bar holds every menu instance. It
        #aligns them all along the top of the window
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        #This takes the newly created Menu Bar and 
        #Tacks it onto the frame holding everything
        self.SetMenuBar(menuBar)
        
        #If you don't know much about Event driven applications
        #Then I recommend reading up on them here:
        #http://en.wikipedia.org/wiki/Event-driven_programming
        
        #These events are what handle each menu item's 
        #resulting actions when clicked. Read the functions
        #(the last arguments passed to each
        #event handler) to get a better idea
        #of how each event works
        
        EVT_MENU(self,ID_OPEN,self.OpenFile)
        EVT_MENU(self,ID_EXIT,self.CloseApp)
        EVT_MENU(self,ID_ABOUT,self.AboutApp)
            
        #This section sets up and starts the Timer
        #This doesn't need to be modified to update more
        #items in the window. Just add whatever else you want
        #updated to the "UpdateTicker" function above
        self.UpdateTimer = wx.Timer(self,ID_TIMER)
        self.UpdateTimer.Start(1)
        wx.EVT_TIMER(self,ID_TIMER,self.UpdateTicker)
        
    #Updates information constantly within the application
    #This allows the Status Bar to be refreshed
    def UpdateTicker(self,event):
        if(self.StatusBar.GetStatusText()!="CWD: " + os.getcwd()):
            self.SetStatusText("CWD: " + os.getcwd())
        
    #Allows the user to open a single file
    def OpenFile(self,event):
        openDialog = wx.FileDialog(self,"Choose an MP3 to open...")
        #openDialog.SetStyle(wx.OPEN)
        typeSearch = "Music Files (.mp3) |*.mp3|"
        openDialog.SetWildcard(typeSearch)
        openDialog.ShowModal()
        currentFileName = openDialog.GetFilename()
        os.chdir(openDialog.GetDirectory())
        openDialog.Destroy()
    
    #Closes the program when a user selects "Exit"
    def CloseApp(self,event):
        self.UpdateTimer.Stop()
        self.Close(True)
        
    #Displays the "About" dialog box
    def AboutApp(self,event):
        #This displays the text, "OK" button, and Window icon for the dialog
        aboutDialog = wx.MessageDialog(self,"Lyrics Lasso\n\nCreated by Timothy 'XBigTK13X' Kretschmer and Bethany Clark\n\nVisit 'http://code.google.com/p/lyricslasso/' for more information.","About")
        aboutDialog.Centre()
        aboutDialog.ShowModal()
        aboutDialog.Destroy()

#wx Applications are basically the "Main" functions
#for wxPython. This class' instance will allow us to 
#control the interaction between the Engine's backend
#and the user's input through the GUI
class mainApp(wx.App):
    #This is called once, the first time the program is run
    def OnInit(self):
        #Creates a new frame instance to hold everything
        frame = mainFrame(None, -1, "Lyrics Lasso")
        #Makes the frame visible
        frame.Show(True)
        #Makes the new frame be displayed above every other window
        self.SetTopWindow(frame)
        #This tells the "MainLoop" that everything was created withou error
        return True

#This sets up a new application for us to utilize
app = mainApp(0)
#This is a function that we will not touch. All of 
#our interaction is done through the events defined
#within the "mainFrame" class
app.MainLoop()