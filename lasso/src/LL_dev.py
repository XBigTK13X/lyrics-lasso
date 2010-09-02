#Development specific functions (logging, debugging, etc)
import logging

#This is a global trigger that tells the program whether or not it should be verbose
DEV_MODE = 1

###################
#Sets up the logger
# To use in any file call as follows
#
#    import LL_dev
#    _L = LL_dev.logger
#    _dP = LL_dev._dP
#    _L.debug("Example debugging message")
#
###################
MIN_LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'll.log'
logging.basicConfig()
logger = logging.getLogger("LyricsLasso")
logger.setLevel(MIN_LOG_LEVEL)
fileHandler = logging.FileHandler(LOG_FILENAME)
logFormat = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fileHandler.setFormatter(logFormat)
logger.addHandler(fileHandler)

#Only prints to the console if development mode is on
def _dP(a):
    if(DEV_MODE):
        print a