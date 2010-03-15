"""
The GUI calls the Engine multiple times 
to handle more than one MP3 at a time
"""

import os
import LL_dev
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
        
        #If you don't know much about Event driven applicaitons
        #Then I recommend reading up on them here:
        #http://en.wikipedia.org/wiki/Event-driven_programming
        
        #Updates information constantly within the application
        #This allows the Status Bar to be refreshed
        def UpdateTicker(event):
            if(self.StatusBar.GetStatusText()!="CWD: " + os.getcwd()):
                self.SetStatusText("CWD: " + os.getcwd())
            
        #This section sets up and starts the Timer
        #This doesn't need to be modified to update more
        #items in the window. Just add whatever else you want
        #updated to the "UpdateTicker" function above
        ID_TIMER = wx.NewId()
        self.UpdateTimer = wx.Timer(self,ID_TIMER)
        self.UpdateTimer.Start(1)
        wx.EVT_TIMER(self,ID_TIMER,UpdateTicker)

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

app = mainApp(0)
#This is a function that we will not touch. All of 
#our interaction is done through the events defined
#within the "mainFrame" class
app.MainLoop()