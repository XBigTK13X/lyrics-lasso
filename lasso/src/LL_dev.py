#Development specific functions (logging, debugging, etc)
import logging

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