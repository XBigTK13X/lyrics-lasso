"""
The Engine is a fully functional console application.
It handles one MP3 at a time.
"""

from mutagen import id3
from mutagen.id3 import ID3
import httplib
import time
import sys
import os
import LL_dev
_dP = LL_dev._dP

#Actually handles the writing of tags
#Saves information in iTunes compatible format
def WriteLyrics(lyrString,curMP3):
    _dP("Writing lyrics...")
    curMP3[u"USLT::'eng'"] = id3.USLT()
    curMP3[u"USLT::'eng'"].text = lyrString
    curMP3[u"USLT::'eng'"].encoding=1
    curMP3[u"USLT::'eng'"].lang = 'eng'
    curMP3[u"USLT::'eng'"].desc=u''
    curMP3.save()
    _dP("ALL FINISHED!")    
    
#This is a built in query service through 'lyricsfly'
#Plugin based architecture (in the future) will provide
#a way to get around copyright restrictions and service
#outages with a single provider
def getData(curMP3):
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

#This function looks up the lyrics for a single track
#Then it embeds those lyrics into the passed MP3 file
def EmbedLyrics(curMP3):
    #Query the database and store resulting repsonse in an object
    data = getData(curMP3)
    #Used to fix IP throttle limitations
    slpTime = 5
    #Basically, just keep waiting longer if your IP is being throttled
    while(data.find("Query too soon!")!=-1):
        _dP("YOU QUERIED TOO QUICKLY!\nWaiting "+str(slpTime)+" seconds and then trying again...")
        time.sleep(slpTime)
        data = getData()
        slpTime+=1
    
    #This section strips the extra data provided
    #By the lyricsfly query and formats everything to look pretty =)
    _dP("Stripping uneeded material from the query response...")
    lyrString = data[data.find("<tx>")+4:data.find("</tx>")-4]
    lyrString = lyrString.replace("[br]","")
    lyrString = lyrString.replace("[... *** Your access is restricted to 30% of content. Please get permanent user ID key for 100% at lyricsfly.com/api/ *** ","")
    lyrString = lyrString.replace("Lyrics delivered by lyricsfly.com ","\n(Lyrics delivered by lyricsfly.com) ")
    lyrString = lyrString.replace("\n\n","\n")
    #Writing newly found lyrics data to the MP3 in iTunes compatible format
    WriteLyrics(lyrString,curMP3)

def StripLyrics(curMP3):
    _dP('Stripping lyrics...')
    WriteLyrics("",curMP3)

def main():
    #Get arguments passed on the command line or from the GUI
    """
    SEPARATE EACH ARGUMENT BY A SINGLE SPACE!!!
    
    argvs
    -----
    [1] = Current Working Directory
    [2] = Current file being lyric analyzed
    [3] = Operation mode
    """
    curDir = sys.argv[1] #string 'c:\xyz\dirName'
    curTarget = sys.argv[2] #string '\filename.mp3'
    opMode = int(sys.argv[3]) #Integer -> 1:x
    if os.getcwd() != curDir:
        os.chdir(curDir)
        
    #This is the single MP3 file being handled at the momenent
    curMP3 = ID3(""+os.getcwd()+"\\"+curTarget+"")
    if opMode == 1:
        EmbedLyrics(curMP3)
        return
    if opMode == 2:
        StripLyrics(curMP3)
        return
    _dP("opMode is out of range!")

#Comment this out for the real application
main()