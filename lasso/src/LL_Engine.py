"""
The Engine is a class used to handle the leg work of manipulating MP3 files
It is GUI independent, and thus is able to be refactored into new GUIs with ease
"""

from mutagen import id3
from mutagen.id3 import ID3
import httplib
import time
import sys
import os
import LL_dev
_L = LL_dev.logger

#Temp key last updated 05/03/2010
apiKey = "dd159059748d3bd16-temporary.API.access"

class Engine():
    #Actually handles the writing of tags
    #Saves information in iTunes compatible format
    def WriteLyrics(self,lyrString,curMP3):
        try:
            _L.debug("Writing lyrics...")
            curMP3[u"USLT::'eng'"] = id3.USLT()
            curMP3[u"USLT::'eng'"].text = lyrString
            curMP3[u"USLT::'eng'"].encoding=1
            curMP3[u"USLT::'eng'"].lang = 'eng'
            curMP3[u"USLT::'eng'"].desc=u''
            curMP3.save()
            _L.debug("ALL FINISHED!")
        except Exception,e:
            _L.error("Writing tag process encountered an error")
            _L.error("EXCEPTION:"+e)
            pass
            pass
        
    #This is a built in query service through 'lyricsfly'
    #Plugin based architecture (in the future) will provide
    #a way to get around copyright restrictions and service
    #outages with a single provider
    def getData(self,curMP3):
        try:
            #The strings inside brackets are the ID tags defined by 'mutagen.id3'
            #See doc for those modules to learn about other tags available
            _L.debug("Querying database. Arist is '"+str(curMP3['TPE2'])+"' and Title is '"+str(curMP3['TIT2'])+"'...")
            connection = httplib.HTTPConnection("api.lyricsfly.com")
            #This if the format to use lyricsfly
            connection.request("GET","/api/api.php?i=" + apiKey + "&a="+str(curMP3['TPE2'])+"&t="+str(curMP3['TIT2'])+"")
            response = connection.getresponse()
            if(response.status is 200):
                _L.debug("QUERY WAS SUCCESSFULLY HANDLED BY THE SITE!")
                data = response.read()
                connection.close()
            else:
                data = "DEAD CONNECTION!"
            return data
        except Exception, e:
            _L.error("Retrieving lyrics tag information from the MP3 failed")
            _L.error("EXCEPTION:"+str(e))
            pass
    
    #This function looks up the lyrics for a single track
    #Then it embeds those lyrics into the passed MP3 file
    def EmbedLyrics(self,curMP3):
        try:
            #Query the database and store resulting repsonse in an object
            data = self.getData(curMP3)
            #Used to fix IP throttle limitations
            slpTime = 5
            #Basically, just keep waiting longer if your IP is being throttled
            while(data.find("Query too soon!")!=-1):
                _L.debug("YOU QUERIED TOO QUICKLY!\nWaiting "+str(slpTime)+" seconds and then trying again...")
                time.sleep(slpTime)
                data = self.getData()
                slpTime+=1
            
            #This section strips the extra data provided
            #By the lyricsfly query and formats everything to look pretty =)
            _L.debug("Stripping uneeded material from the query response...")
            lyrString = data[data.find("<tx>")+4:data.find("</tx>")-4]
            lyrString = lyrString.replace("[br]","")
            lyrString = lyrString.replace("[... *** Your access is restricted to 30% of content. Please get permanent user ID key for 100% at lyricsfly.com/api/ *** ","")
            lyrString = lyrString.replace("Lyrics delivered by lyricsfly.com ","\n(Lyrics delivered by lyricsfly.com) ")
            lyrString = lyrString.replace("\n\n","\n")
            #Writing newly found lyrics data to the MP3 in iTunes compatible format
            self.WriteLyrics(lyrString,curMP3)
        except Exception,e:
            _L.error("An engine error occurred while attempting to embed the lyrics tag")
            _L.error("EXCEPTION: "+str(e))
            pass
    
    #Remove lyrics from the MP3 file
    def StripLyrics(self,curMP3):
        _L.debug('Stripping lyrics...')
        self.WriteLyrics("",curMP3)
    
    #Prevents bad access of a non-existent lyrics tag
    def CreateLyricsTag(self,curMP3):
        curLyr="Empty"
        #This protects us from reading a non-existence key entry in the ID3 tag
        while(curLyr=="Empty"):
            try:
                curLyr = curMP3[u"USLT::'eng'"].text
                break;
            except KeyError:
                curLyr = curMP3[u"USLT::'eng'"] = id3.USLT()
        return curLyr
    
    #Retrieves the lyrics tag stored in the current MP3 file
    def GetLyrics(self,curMP3):
        self.CreateLyricsTag(curMP3)
        return curMP3[u"USLT::'eng'"].text
    
    #Returns the current state of lyrics existence for the curMP3 file
    def HasLyrics(self,curMP3):
        curLyr = self.CreateLyricsTag(curMP3)
        _L.debug('Checking MP3s lyrics status...')
        if(curLyr == "" or self.GetLyrics(curMP3)==id3.USLT().text):
            _L.debug("Lyrics don't exist in the current MP3 file!")
            return "No"
        else:
            _L.debug("Lyrics exist!")
            return "Yes"
        
	# This Function simply returns an ID3 Mp3 object
	# when given a file location. 
	def GetMp3(self, mp3Directory, mp3Filename):
		return ID3(""+mp3Directory+"\\"+mp3Filename+"")
		
    def main(self,argv):
        _L.info("Starting the engine")
        #Get arguments passed on the command line or from the GUI
        """
        SEPARATE EACH ARGUMENT BY A SINGLE SPACE!!!
        
        argvs
        -----
        [1] = Current Working Directory
        [2] = Current file being lyric analyzed
        [3] = Operation mode
        """
        if(len(argv)==3):#simple error checking, noone should be accessing the binary by itself
                                #so we don't need much error checking
            curDir = argv[0] #string 'c:\xyz\dirName'
            curTarget = argv[1] #string '\filename.mp3'
            opMode = int(argv[2]) #Integer -> 1:x
            print argv[0]
            print argv[1]
            print argv[2]
            if os.getcwd() != curDir:
                os.chdir(curDir)
        else:
            _L.debug("INCORRECT NUMBER OF ARGUMENTS PASSED!\nUSAGE: 'LL_Engine.py path file opMode'\nExiting...")
            return
        #This is the single MP3 file being handled at the momenent
        curMP3 = ID3(""+os.getcwd()+"\\"+curTarget+"")
        if opMode == 1:
            self.EmbedLyrics(curMP3)
            return
        elif opMode == 2:
            self.StripLyrics(curMP3)
            return
        elif opMode == 3:
            return self.HasLyrics(curMP3)
        elif opMode == 4: 
            return self.GetLyrics(curMP3)
        else:
            _L.debug("opMode IS OUT OF RANGE!")