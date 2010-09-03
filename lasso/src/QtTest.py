#!/usr/bin/python

# icon.py

import sys
from PyQt4 import QtGui, QtCore


class TooltipTest(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        # Set up the main window.
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit Button Test')
        self.setWindowIcon(QtGui.QIcon('icons/web.png'))
        # Set the tooltip for the main window. Why? Who knows?
        self.setToolTip('<p>This is a <b>QWidget</b> widget</p><p>QWidgets are the basic uilding blocks of PyQt4 classes.</p>')
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
        
        # Status Bar
        self.statusBar().showMessage('Ready')
        
        # Menu Bar
        exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(exit)
        
        # Quit Button.
        quitButton = QtGui.QPushButton('Quit This Sucka Yo', self)
        quitButton.setGeometry(50,80,120,45)
        self.connect(quitButton, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('buttonReaction()'))
        
        # Test Button.
        #quitButton = QtGui.QPushButton('Quit This Sucka Yo', self)
        #quitButton.setGeometry(50,50,120,45)
        #self.connect(quitButton, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('buttonReaction()'))
        
        # Toolbar.
        self.dice = QtGui.QAction(QtGui.QIcon('icons/dice.png'), 'Roll \'Em', self)
        self.mrt = QtGui.QAction(QtGui.QIcon('icons/mrt.png'), 'Pity the Fool', self)
        self.book = QtGui.QAction(QtGui.QIcon('icons/book.jpg'), 'Read', self)
        self.green = QtGui.QAction(QtGui.QIcon('icons/green.png'), 'Go Green?', self)
        
        self.toolbar = self.addToolBar('Main')
        self.toolbar.addAction(self.dice)
        self.toolbar.addAction(self.mrt)
        self.toolbar.addAction(self.book)
        self.toolbar.addAction(self.green)
        
        # Main Widget - a Text Editor?
        #textEdit = QtGui.QTextEdit()
        #self.setCentralWidget(textEdit)
        
        # Set tooltip for the button. Some people don't know what "Quit This Sucka Yo" means.
        quitButton.setToolTip('Click this sucka to quit <i>this</i> sucka.')
    
    def buttonReaction(self):
        print "Button Clicked"

app = QtGui.QApplication(sys.argv)
widget = TooltipTest()
widget.show()
sys.exit(app.exec_())