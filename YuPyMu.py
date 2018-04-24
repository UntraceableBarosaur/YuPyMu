# Owen Cody, 4-04-2018, Python

# Overview :
# YuPyMu was created as a GUI program to download and tag music
# ripped from a given youtube url for addition to MP3 Players

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

# Attempt to import necessary packages
from __future__ import unicode_literals
import youtube_dl
import os
import shutil
import requests

import PIL.Image

from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, COMM, USLT, TCOM, TCON, TDRC, APIC, error


# --- Set Global Variables to be referenced in all areas ---
global albumName
global prgmPath
global ydlDataStorage
global replaceString
global trackcount
global totaltracks
global replaceFirst
# --- Set Parameters
prgmPath = os.getcwd()

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

# --- Install prerequisites ---

# (This section in `if __name__ == '__main__':` is entirely unrelated to the
# rest of the module, and doesn't even run if the module isn't run by itself.)

if __name__ == '__main__':
    import imp # To check modules without importing them.

    requiredModules = [
        ['requests', 'requests'], # Some modules don't have the same pypi name as
        ['youtube_dl', 'youtube-dl'],  # import name. Therefore, two entries per module.
        ['mutagen', 'mutagen'],
        ['PIL', 'Imaging']
    ]

    def moduleExists(module):
        try:
            imp.find_module(module[0])
        except ImportError:
            return False
        return True
    def neededInstalls(requiredModules=requiredModules):
        uninstalledModules = []
        for module in requiredModules:
            if not moduleExists(module):
                uninstalledModules.append(module)
        return uninstalledModules

    def install(package):
        pip.main(['install', '--quiet', package])
    def installModules(modules, verbose=True):
        for module in modules:
            if verbose:
                print("Installing {}...".format(module[1]))
            install(module[1])
    def installRequiredModules(needed=None, verbose=True):
        needed = neededInstalls() if needed is None else needed
        installModules(neededInstalls(), verbose)

    needed = neededInstalls()
    if needed: # Only import pip if modules are actually missing.
        try:
            import pip # To install modules if they're not there.
        except ImportError:
            print("You don't seem to have pip installed!")
            print("Get it from https://pip.readthedocs.org/en/latest/installing.html")

    installRequiredModules(needed)

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# ------ URL Prompt

downloadStorage = str(raw_input("Insert Downloadable Url:     "))
albumName = str(raw_input("Insert Album Name:     "))
albumName = albumName.replace("OST", "( Original Soundtrack )")
replaceFirst = int(raw_input("Replace first x characters:     "))
totaltracks = int(raw_input("Total Number of Tracks:     "))
replaceString = str(raw_input("Do you want to replace a header:     "))
if(replaceString == "n"):
    print("do not replace string")
    replaceString = "DO_NOT"
else:
    print("replacing string")
    print(replaceString)

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

def getListedVariable(inputList,defaultName):
    for x in range(0,len(inputList)):
        try:
            if(inputList[x] in ydlDataStorage):
                defaultName = str(ydlDataStorage['entries'][0][inputList[x]].encode('ascii', 'ignore'))
                if(defaultName == "None"):
                    print(inputList[x])
                    print(str(ydlDataStorage['entries'][0][inputList[x]].encode('ascii', 'ignore')))
                else:
                    if(inputList[x] == 'upload_date'):
                        defaultName[:4]
                    defaultName = defaultName.replace('"','')
                    return defaultName
            if(inputList[x] == 'require_input'):
                defaultName = str(raw_input("Please enter the "+str(inputList[0])+":       "))
                return defaultName
            if(inputList[x] == 'albumName'):
                return albumName
        except KeyError:
            print(inputList[x]+' caused a nasty error!')
    return defaultName

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
#CONFIGS

trackArtistInputVars = ['artist','creator','uploader','uploader_id']
trackTitleInputVars = ['track','alt_title','track_id','title']
trackAlbumInputVars = ['album','albumName', 'require_input']
trackComposerInputVars = ['creator','artist','uploader','uploader_id']
trackTrackInputVars = ['track_number','playlist_index']
trackYearInputVars = ['release_year','upload_date']
# ------ Extract strings direct from ydl json file

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
def formatSong(ydlDataStorage):
    imagefname = str(prgmPath+"/"+albumName+"/"+'Track_'+str(trackcount)+".jpg")
    print("Thumbnail path for Track # "+str(trackcount)+" : ")
    print(imagefname)
    fname = str(prgmPath+"/"+albumName+"/"+'Track_'+str(trackcount)+".mp3")
    fname = fname.replace(":"," -")
    fname = fname.replace('None',"NA")
    fname = fname.replace("|","_")
    print("File path for Track # "+str(trackcount)+" : ")
    print(fname)
    #trackCategories = "36"
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    response = requests.get(str('https://i.ytimg.com/vi/'+str(ydlDataStorage['entries'][0]['id'])+'/maxresdefault.jpg'), stream=True)
    with open(imagefname, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    THUMB_SIZE = 360, 360
    img = PIL.Image.open(imagefname)
    width, height = img.size

    if width > height:
       delta = width - height
       left = int(delta/2)
       upper = 0
       right = height + left
       lower = height
    else:
       delta = height - width
       left = 0
       upper = int(delta/2)
       right = width
       lower = width + upper

    img = img.crop((left, upper, right, lower))
    img.thumbnail(THUMB_SIZE, PIL.Image.ANTIALIAS)
    img.save(imagefname)
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    # create ID3 tag if not present
    try:
        tags = ID3(fname)
    except ID3NoHeaderError:
        print "Adding ID3 header;",
        tags = ID3()

    tags["APIC"] = APIC(encoding=3, mime='image/jpeg', desc=u'%s'%(imagefname), data=open(imagefname).read())
    tags["TIT2"] = TIT2(encoding=3, text=u'%s'%(getListedVariable(trackTitleInputVars,"Unknown Title").replace(replaceString,"")[int(replaceFirst):]))
    tags["TALB"] = TALB(encoding=3, text=u'%s'%(getListedVariable(trackAlbumInputVars,"Unknown Album")))
    tags["TPE1"] = TPE1(encoding=3, text=u'%s'%(getListedVariable(trackArtistInputVars,"Unknown Artist")))
    tags["TCOM"] = TCOM(encoding=3, text=u'%s'%(getListedVariable(trackComposerInputVars,"Unknown Composer")))
    tags["TDRC"] = TDRC(encoding=3, text=u'%s'%(getListedVariable(trackYearInputVars,"2000")))
    tags["TRCK"] = TRCK(encoding=3, text=u'%s'%(str(trackcount)+"/"+str(totaltracks)))
    #tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text=u'mutagen comment')
    #tags["TCON"] = TCON(encoding=3, text=u'%s'%(trackCategories))

    tags.save(fname)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""




"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# ------

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done Downloading, Now Converting ...')

# ------
trackcount=0
while(trackcount<totaltracks):
    trackcount=trackcount+1
    ydl_opts = {
        'outtmpl': str(albumName + '/Track_'+str(trackcount) +'.%(ext)s'),
        'format': 'bestaudio/best',
        'playlist_items': str(trackcount),
        'noplaylist' : True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Initializing Download Of Track # " + str(trackcount)+" ...")
        ydl.download([downloadStorage])
        print("Finished Converting, Adding Info...")
        ydlDataStorage = ydl.extract_info(downloadStorage, download=False)  # don't download, much faster
        print(str(ydlDataStorage['entries'][0]['id']))
        formatSong(ydlDataStorage)
        print("Information Written, Continuing On To Next Track...")
print("Finished...")
