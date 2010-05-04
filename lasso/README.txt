(I) Dependencies
    a) wxPython
    b) Python modules
        i) mutagen
(II) Building Binaries

--------------------------
(I) - Dependencies
==========================

    (a) wxPython (Python wxWidgets port)
    
        ---
        Win
        ===
        Grab the appropriate wxPython binary from:
        http://www.wxpython.org/download.php#binaries
        
        ----------------
        GNU/Lin (Ubuntu)
        ================
        1) sudo synaptic
        2) Install the "python-wxgtkX.X" package,
           with X.X being your installed python version
    
    (b) Python Modules
        i) mutagen (http://code.google.com/p/mutagen/downloads/list)
   
-------------------------
(II) Building Binaries
=========================

    Although Lyrics Lasso is a fully functional Python script based program,
    it is easiest for end users to utilize the program by running a precompiled
    binary.
    
    -----------------
    Win32 Compilation
    =================
        Prereqs: http://sourceforge.net/projects/py2exe/
        
        
        Use this script to build on Windows.
        ========
        setup.py
        ========
        from distutils.core import setup
        import py2exe
        setup(windows=['LL_main.py'])
        
        To build on Windows enter the following on the Command Prompt
        
        'python setup.py py2exe'
        
    --------------------------
    Lin32 (Ubuntu) Compilation
    ==========================
    