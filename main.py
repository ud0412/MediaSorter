
import os
import exifread
import time

DT_TAGS = ["Image DateTime", "EXIF DateTimeOriginal", "DateTime"]
PictureType = [".jpg", ".png", ".gif"]
MovieType = [".mov", ".avi", ".mp4", ".mkv"]
UnsupportType = ["", ".py", ".json", ".cfg", ".md", ".ini", ".in", ".html", ".js", ".css", ".sh", ".yml", ".pack", ".idx", ".sample", ".gz", ".meta", ".mp3"]

def isUnsupported(file) :
    name, ext = os.path.splitext(file)
    if ext.lower() in UnsupportType :
        return True
    return False

def isPicture(file) :
    name, ext = os.path.splitext(file)
    if ext.lower() in PictureType :
        return True
    return False

def isMovie(file) :
    name, ext = os.path.splitext(file)
    if ext.lower() in MovieType :
        return True
    return False

def getFilesList(path, list) :
    fs = os.listdir(path)
    
    for f in fs :
        f = os.path.join(path, f)
        if os.path.isdir(f) :
            getFilesList(f, list)
        else:
            list.append(f)

def getImageDate(f) :
    with open(f, "rb") as image :
        tags = exifread.process_file(image)
        dt_value = None
        for dt_tag in DT_TAGS:
            try:
                dt_value = '%s' % tags[dt_tag]
                break
            except:
                continue
        
        if dt_value:
            exif_time = time.strptime(dt_value + 'UTC', '%Y:%m:%d %H:%M:%S%Z')
            return exif_time

basedir = os.path.join("/", "media", "ud0412", "Data", "Picture")

files = []
getFilesList(basedir, files)
for f in files:
    if isUnsupported(f) :
        continue
    elif isPicture(f) :
        t = getImageDate(f)
        if t:
            #print t
            continue
        else:
            print f
    elif isMovie(f) :
        #print f
        continue
    else :
        continue
