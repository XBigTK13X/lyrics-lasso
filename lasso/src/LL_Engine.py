"""
The Engine is a fully functional console application.
It handles one MP3 at a time.
"""

from mutagen import id3
from mutagen.id3 import ID3
import httplib
import time
import sys
import getopt
import os


#Debugging Variables
DEV_MODE = 1 #This will quiet all the "print" statements

#iff Dev Mode on, then output to screen
def _dP(a):
    if(DEV_MODE):
        print a
def main():
    #This is the single MP3 file being handled at the momenent
    _dP(os.getcwd())
    curMP3 = ID3("C:\Users\KRETST\Documents\workspace\Lyrics_Lasso\src\example.mp3")
    
    #This is a built in query service through 'lyricsfly'
    #Plugin based architecture (in the future) will provide
    #a way to get around copyright restrictions and service
    #outages with a single provider
    def getData():
        #The strings inside brackets are the ID tags defined by 'mutagen.id3'
        #See doc for those modules to learn about other tags available
        _dP("Querying database. Arist is '"+str(curMP3['TPE2'])+"' and Title is '"+str(curMP3['TIT2'])+"'...")
        connection = httplib.HTTPConnection("api.lyricsfly.com")
        #This if the format to use lyricsfly
        connection.request("GET","/api/api.php?i=e9058775b534412ca-temporary.API.access&a="+str(curMP3['TPE2'])+"&t="+str(curMP3['TIT2'])+"")
        response = connection.getresponse()
        if(response.status is 200):
            _dP("QUERY WAS SUCCESSFULLY HANDLED BY THE SITE!")
            data = response.read()
            connection.close()
        else:
            data = "DEAD CONNECTION!"
        return data
    
    #Query the database and store resulting repsonse in an object
    data = getData()
    #Used to fix IP throttle limitations
    slpTime = 5
    #Basically, just keep waiting longer if your IP is being throttled
    while(data.find("Query too soon!")!=-1):
        _dP("YOU QUERIED TOO QUICKLY!\nWaiting "+str(slpTime)+" seconds and then trying again...")
        time.sleep(slpTime)
        data = getData()
        slpTime+=1
    
    #This section strips the extra data provided
    #By the lyricsfly query    
    _dP("Stripping uneeded material from the query response...")
    lyrString = data[data.find("<tx>")+4:data.find("</tx>")-4]
    lyrString = lyrString.replace("[br]","")
    lyrString = lyrString.replace("[... *** Your access is restricted to 30% of content. Please get permanent user ID key for 100% at lyricsfly.com/api/ *** ","")
    lyrString = lyrString.replace("Lyrics delivered by lyricsfly.com ","\n(Lyrics delivered by lyricsfly.com) ")
    
    #Prints out the current state of the formatted lyrics string
    #_dP(lyrString)
    
    #Writing newly found lyrics data to the MP3 in iTunes compatible format
    _dP("Writing tag...")
    curMP3[u"USLT::'eng'"] = id3.USLT()
    curMP3[u"USLT::'eng'"].text  = lyrString
    curMP3[u"USLT::'eng'"].encoding=1
    curMP3[u"USLT::'eng'"].lang = 'eng'
    curMP3[u"USLT::'eng'"].desc=u''
    curMP3.save()
    _dP("ALL FINISHED!")
