"""
The GUI calls the Engine multiple times 
to handle more than one MP3 at a time
"""

import os
import sys
import LL_dev
import LL_Engine
from mutagen.id3 import ID3
from PyQt4 import QtGui, QtCore
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

#These global variables will be used to track the 
#current working directory and current working file
currentFileName = ""
ENGINE = LL_Engine.Engine()

#This is the bulk of the GUI's programming
#This will be the class used to generate 
#The application's main frame


class mainFrame(QtGui.QtWidget):
    #Standard class requirement
    #This function is what is called when
    #creating a new instance of a class
    def __init__(self, parent=None, title):
        #This creates a new frame. Frames are what hold everything
        #you see in an application's window
        QtGui.QMainWindow.__init__(self, parent)
        self.SetGeometry(600, 450, 250, 250)
        self.setWindowTitle(title)

        #This generates a status bar (The thing in the window
        #that displays the current working directory)
        self.statusBar().showMesage("CWD: "+os.getcwd())
        
        #The Menu Bar holds every menu instance. It
        #aligns them all along the top of the window
        menuBar = self.menuBar()
        
        #Menus are what contain various actions at the top
        #of a window. In Eclipse, "File", "Edit", etc. are each 
        #a separate menu entity
        fileMenu = menuBar.addMenu('&File')
        changeDir = QtGui.QAction(QtGui.QIcon('icons/chngdir.png'), 'Change &Directory', self) # fileMenu.Append(ID_OPENDIR, "Change &Directory")
        addMp3 = QtGui.QAction(QtGui.QIcon('icons/mp3duck.png'), '&Add Mp3 File', self)# fileMenu.Append(ID_OPENFILE, "&Append File")
        clearAll = QtGui.QAction(QtGui.QIcon('icons/clear.png'), '&Clear All', self)# fileMenu.Append(ID_CLEAR, "&Clear All")
        writeAll = QtGui.QAction(QtGui.QIcon('icons/write.png'), '&Write All', self)# fileMenu.Append(ID_WRITE, "&Write All")
        exitOption = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self) # fileMenu.Append(ID_EXIT, "E&xit")
        
        #Another Menu
        helpMenu = menuBar.addMenu('&Help')
        changeDir = QtGui.QAction(QtGui.QIcon('icons/about.png'), '&About', self) # helpMenu.Append(ID_ABOUT, "&About")
		
        # Here's where I'm at.
        # I need to figure out the self.connect() functions for each of these guys.
        #------------------------------------------------------------------------------------
        
        
        # Right click menu titles
        rightClickTitles = ["Write Lyrics", "Remove Lyrics"]
        self.rightClickIds = {}
        for title in rightClickTitles:
            self.rightClickIds[ wx.NewId() ] = title
        
        #This list control is what displays
        #all of the information about the
        #files in the CWD
        #mp3List = wx.ListBox(self)
        windowSize = self.GetVirtualSize()
        
        self.mp3List = wx.ListCtrl(self, style = wx.LC_REPORT, size=(math.floor(windowSize[0]*0.7),windowSize[1]))
        self.FillList()
        
        #If you don't know much about Event driven applications
        #Then I recommend reading up on them here:
        #http://en.wikipedia.org/wiki/Event-driven_programming
        
        #These events are what handle each menu item's 
        #resulting actions when clicked. Read the functions
        #(the last arguments passed to each
        #event handler) to get a better idea
        #of how each event works
        
        EVT_MENU(self,ID_OPENFILE,self.OpenFile)
        EVT_MENU(self,ID_OPENDIR,self.OpenDirectory)
        EVT_MENU(self,ID_EXIT,self.CloseApp)
        EVT_MENU(self,ID_ABOUT,self.AboutApp)
        EVT_MENU(self,ID_CLEAR,self.ClearAll)
        EVT_MENU(self,ID_WRITE,self.WriteAll)
        EVT_MENU(self,ID_SHOW_LYRICS,self.LyricsDialog)
        
        # Event binding for Right Clicks.
        EVT_LIST_ITEM_RIGHT_CLICK(self.mp3List, -1, self.RightClickEvent)
        self.listItemClicked = None
        # Event binding for Left Clicks.
        EVT_LIST_ITEM_SELECTED(self.mp3List, -1, self.ShowLyrics)
        
        
        #This section sets up and starts the Timer
        #This doesn't need to be modified to update more
        #items in the window. Just add whatever else you want
        #updated to the "UpdateTicker" function below
        self.UpdateTimer = wx.Timer(self,ID_TIMER)
        self.UpdateTimer.Start(1)
        wx.EVT_TIMER(self,ID_TIMER,self.UpdateTicker)
        
        # The following is a side panel which will show 
        # currently selected song's lyrics. 
        #self.lyricsPanel = wx.TextCtrl(self, size=(math.floor(windowSize[0]*0.3),windowSize[1]), style=wx.TE_MULTILINE | wx.TE_READONLY, value="No File Selected.")
        self.lyricsPanel = wx.TextCtrl(self, size=(200,windowSize[1]), style=wx.TE_MULTILINE | wx.TE_READONLY, value="No File Selected.")
        
        # Here the layout of the panels is set up. 
        self.mainSizer = wx.GridSizer(1,2,4,4)
        self.mainSizer.Add(self.mp3List, 0, wx.ALIGN_LEFT)
        self.mainSizer.Add(self.lyricsPanel, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(self.mainSizer)
        
    #Handles the right click context menu for each item in the ListCtrl
    def RightClickEvent(self, event):
        self.listItemClicked = right_click_context = event.GetText()
        rightClickMenu = wx.Menu()
        for (id, title) in self.rightClickIds.items():
            rightClickMenu.Append(id, title)
            EVT_MENU(rightClickMenu, id, self.ActionSelect)
        
        self.PopupMenu(rightClickMenu, event.GetPoint())
        rightClickMenu.Destroy()
        
    def ActionSelect(self, event):
        operation = self.rightClickIds[event.GetId()]
        # target = self.listItemClicked
        target = self.mp3List.GetFirstSelected()
        curSong = self.mp3List.GetItemText(target)
        _dP("'" + operation + "' on '" + curSong + "'")
        if "Write" in operation:
            #print 'in here'
            ENGINE.main([os.getcwd(),curSong,1])
        elif "Remove" in operation:
            #print 'over here'
            ENGINE.main([os.getcwd(),curSong,2])
        else:
            _dP('unknown right click operation')
    
    # This Function simply returns an ID3 Mp3 object
    # when given a file location. 
    def GetMp3(self, mp3Directory, mp3Filename):
        return ID3(""+mp3Directory+"\\"+mp3Filename+"")
    
    # This Function will display the lyrics of the currently
    # selected song in the lyricsPanel. 
    def ShowLyrics(self, event):
        event.GetId()
        target = self.mp3List.GetFirstSelected()
        #target = event.GetText()
        title = self.mp3List.GetItemText(target)
        
        lyricsText = ENGINE.GetLyrics(ID3(""+os.getcwd()+"\\"+title+""))
        
        self.lyricsPanel.ChangeValue(lyricsText)				
        _dP("Displaying Lyrics for " + title + ".")
	
    # This Function will clear the lyricsPanel. 
    def ClearLyrics(self,event):
        self.lyricsPanel.ChangeValue("No Lyrics To Display")				
        _dP("Clearing Lyrics Box.")
	
    # This Function will dynamically resize the wondow based on its current state.
    def Resize(self):
        windowSize = self.GetVirtualSize()
        # A few lines that I can't get to work:
        #self.lyricsPanel.SetSize((math.floor(windowSize[0]*0.3),windowSize[1]))
        #self.mp3List.SetSize((math.floor(windowSize[0]*0.7),windowSize[1]))
        
        # The best working form I can come up with.
        self.lyricsPanel.SetSize((200,windowSize[1]))
        self.mp3List.SetSize((math.floor(windowSize[0]-204),windowSize[1]))
        #Issue: LyricsPanel refuses to change width. Changing its width either does nothing or moves it sideways.
    
    #Updates information constantly within the application
    #This allows the Status Bar to be refreshed
    def UpdateTicker(self,event):
        if(self.StatusBar.GetStatusText()!="CWD: " + os.getcwd()):
            self.SetStatusText("CWD: " + os.getcwd())
        self.Resize()
    
    #Allows the user to open a single file
    def OpenFile(self,event):
        openDialog = wx.FileDialog(self,"Choose an MP3 to open...")
        #openDialog.SetStyle(wx.OPEN)
        typeSearch = "Music Files (.mp3) |*.mp3|"
        openDialog.SetWildcard(typeSearch)
        openDialog.ShowModal()
        #DELETE-currentFileName = openDialog.GetFilename()
        self.AppendToList(openDialog.GetFilename(),openDialog.GetDirectory())
        openDialog.Destroy()
    
    #Allows the user to open a directory
    def OpenDirectory(self,event):
        openDialog = wx.DirDialog(self,"Choose a directory to open...")
        #openDialog.SetStyle(wx.OPEN)
        #DEL typeSearch = "Music Files (.mp3) |*.mp3|"
        #DELopenDialog.SetWildcard(typeSearch)
        openDialog.ShowModal()
        #DELETE-currentFileName = openDialog.GetFilename()
        os.chdir(openDialog.GetPath())
        self.FillList()
        openDialog.Destroy()
    
    #Closes the program when a user selects "Exit"
    def CloseApp(self,event):
        self.UpdateTimer.Stop()
        self.Close(True)
        
    #Displays the "About" dialog box
    def AboutApp(self,event):
        #This displays the text, "OK" button, and Window icon for the dialog
        aboutDialog = wx.MessageDialog(self,"Lyrics Lasso\n\nCreated by Timothy 'XBigTK13X' Kretschmer, Ken Bellows, and Mike Stark.\n\nVisit 'http://code.google.com/p/lyricslasso/' for more information.","About")
        aboutDialog.Centre()
        aboutDialog.ShowModal()
        aboutDialog.Destroy()
        
    #Tries to find and write lyrics to every file in the ListCtrl
    def WriteAll(self,event):
        for i in range(self.mp3List.GetItemCount()):
            curMP3 = self.mp3List.GetItem(i,0).GetText()
            _dP(curMP3 + "____" + os.getcwd() + "____")
            self.mp3List.SetStringItem(i,1,ENGINE.main([os.getcwd(),str(curMP3),1]))
            
    #Strips the lyrics out of all the files in the ListCtrl        
    def ClearAll(self,event):
        for i in range(self.mp3List.GetItemCount()):
            curMP3 = self.mp3List.GetItem(i,0).GetText()
            ENGINE.main([os.getcwd(),str(curMP3),2])
            self.mp3List.SetStringItem(i,1,"No")
    
    #Displays the lyrics of the currently highlighted file
    def LyricsDialog(self,event):
        curItem = self.mp3List.GetFirstSelected()
        if(curItem!=-1):
            curMP3 = self.mp3List.GetItemText(curItem)
            curPath = self.mp3List.GetItem(curItem,2)
            curPath = curPath.GetText()
            oCWD = os.getcwd()
            os.chdir(curPath)
            diag = wx.MessageDialog(self,ENGINE.main([os.getcwd(),curMP3,4]),"Lyrics Viewer")
            diag.Centre()
            diag.ShowModal()
            diag.Destroy()
            os.chdir(oCWD)    

    #Appends a single MP3 file to the ListCtrl
    def AppendToList(self,curMP3,curPath):
        hasL = ENGINE.main([curPath,str(curMP3),3])
        self.mp3List.InsertStringItem(self.mp3List.GetItemCount(),str(curMP3))
        self.mp3List.SetStringItem(self.mp3List.GetItemCount()-1,1,str(hasL))
        self.mp3List.SetStringItem(self.mp3List.GetItemCount()-1,2,str(curPath))
        
    #Populates the List Control with the the CWD's mp3 files
    def FillList(self):
        self.mp3List.ClearAll()
        self.mp3List.InsertColumn(0,"Filename")
        self.mp3List.InsertColumn(1,"Has Lyrics")
        self.mp3List.InsertColumn(2,"Path")
        rawList = os.listdir(os.getcwd())
        for i in range(len(rawList)):
            if(str(rawList[i]).find(".mp3")!=-1):
                hasL = ENGINE.main([os.getcwd(),str(rawList[i]),3])
                self.mp3List.InsertStringItem(self.mp3List.GetItemCount(),str(rawList[i]))
                self.mp3List.SetStringItem(self.mp3List.GetItemCount()-1,1,str(hasL))
                self.mp3List.SetStringItem(self.mp3List.GetItemCount()-1,2,str(os.getcwd()))
				
#wx Applications are basically the "Main" functions
#for wxPython. This class' instance will allow us to 
#control the interaction between the Engine's backend
#and the user's input through the GUI
class mainApp(wx.App):
    #This is called once, the first time the program is run
    def OnInit(self):
        #Creates a new frame instance to hold everything
        frame = mainFrame(title="Lyrics Lasso")
        #Makes the frame visible
        frame.Show(True)
        #Makes the new frame be displayed above every other window
        self.SetTopWindow(frame)
        #This tells the "MainLoop" that everything was created without error
        return True

#This sets up a new application for us to utilize
app = mainApp(0)
#This is a function that we will not touch. All of 
#our interaction is done through the events defined
#within the "mainFrame" class
app.MainLoop()