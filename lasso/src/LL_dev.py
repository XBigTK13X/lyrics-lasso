#These are development specific variables and functions

#This is a global trigger that tells the program whether or not it should be verbose
DEV_MODE = 1

#Only prints to the console if development mode is on
def _dP(a):
    if(DEV_MODE):
        print a