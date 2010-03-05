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
wxWidgets dependencies correctly

See the README for help
"""

# Original framework producded with wxGlade
# generated by wxGlade 0.6.3 on Fri Mar 05 10:41:18 2010

from wxPython.wx import *



class wxFrame(wxFrame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxFrame.__init__
        kwds["style"] = wxDEFAULT_FRAME_STYLE
        
        # Menu Bar
        self.frame_2_menubar = wxMenuBar()
        self.file = wxMenu()
        self.chdir = wxMenuItem(self.file, chdir, "Change Directory", "", wxITEM_NORMAL)
        self.file.AppendItem(self.chdir)
        self.frame_2_menubar.Append(self.file, "File")
        self.SetMenuBar(self.frame_2_menubar)
        # Menu Bar end
        self.frame_2_statusbar = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.frame_2_toolbar = wxToolBar(self, -1)
        self.SetToolBar(self.frame_2_toolbar)
        self.frame_2_toolbar.AddLabelTool(wxNewId(), "chdir", wxBitmap("C:\\Users\\KRETST\\Documents\\workspace\\Lyrics_Lasso\\src\\GFX\\chdir.bmp", wxBITMAP_TYPE_ANY), wxBitmap("C:\\Users\\KRETST\\Documents\\workspace\\Lyrics_Lasso\\src\\GFX\\chdir.bmp", wxBITMAP_TYPE_ANY), wxITEM_NORMAL, "", "")
        # Tool Bar end
        self.fileList = wxListCtrl(self, -1, style=wxLC_REPORT|wxSUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxFrame.__set_properties
        self.SetTitle("Lyrics Lasso")
        self.SetSize((600, 555))
        self.SetFocus()
        self.frame_2_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_2_statusbar_fields = ["Current working directory:"]
        for i in range(len(frame_2_statusbar_fields)):
            self.frame_2_statusbar.SetStatusText(frame_2_statusbar_fields[i], i)
        self.frame_2_toolbar.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxFrame.__do_layout
        sizer_1 = wxBoxSizer(wxVERTICAL)
        sizer_1.Add(self.fileList, 1, wxEXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

# end of class wxFrame


class LyricsLasso(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        frame_1 = wxFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class LyricsLasso
if(LL_dev.DEV_MODE):
    if __name__ == "__main__":
        LyricsLasso = LyricsLasso(0)
        LyricsLasso.MainLoop()
