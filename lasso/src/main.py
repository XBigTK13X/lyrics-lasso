from mutagen.mp3 import MP3
from mutagen import id3
from mutagen.id3 import ID3
import httplib
audio = ID3("example.mp3")
print audio["TIT2"]

connection = httplib.HTTPConnection("api.lyricsfly.com")
connection.request("GET","/api/api.php?i=e9058775b534412ca-temporary.API.access&a="+str(audio['TPE2'])+"&t="+str(audio['TIT2'])+"")
response = connection.getresponse()
if(response.status is 200):
    data = response.read()
    connection.close()
else:
    print "Dangit! The connection failed!"
    
lyrString = data[data.find("<tx>")+4:data.find("</tx>")-4]
if(data.find("Query too soon!")!=-1):
    print "You queried too quickly!"
    
else:
    lyrString = lyrString.replace("[br]","")
    lyrString = lyrString.replace("[... *** Your access is restricted to 30% of content. Please get permanent user ID key for 100% at lyricsfly.com/api/ *** ","")
    lyrString = lyrString.replace("Lyrics delivered by lyricsfly.com ","\n(Lyrics delivered by lyricsfly.com) ")
    print lyrString
    audio[u"USLT::'eng'"] = id3.USLT()
    audio[u"USLT::'eng'"].text  = lyrString
    audio[u"USLT::'eng'"].encoding=1
    audio[u"USLT::'eng'"].lang = 'eng'
    audio[u"USLT::'eng'"].desc=u''
    audio.save()

    

# TPE2(TextFrame): "Artist"
# TIT2(TextFrame): "Title"