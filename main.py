
import os
import exifread
import time
from libxmp.utils import file_to_dict
import hashlib

DT_TAGS = ["Image DateTime", "EXIF DateTimeOriginal", "DateTime"]
PictureType = [".jpg", ".png", ".gif"]
MovieType = [".mov", ".avi", ".mp4", ".mkv"]
UnsupportType = ["", ".py", ".json", ".cfg", ".md", ".ini", ".in", ".html", ".js", ".css", ".sh", ".yml", ".pack", ".idx", ".sample", ".gz", ".meta", ".mp3"]

hashs = {}
basedir = os.path.join("/", "media", "ud0412", "Data", "Picture")
targetBase = "/media/ud0412/Data/target"

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

def getMovieDate(f):
    xmp_info_list = file_to_dict(f)
    for xmp_info in xmp_info_list:
        for element in xmp_info_list[xmp_info]:
            for element_data in element:
                if "xmp:CreateDate" in element_data:
                    source_file_created_date = element[1][:]
                    return source_file_created_date.replace("-", "").replace("T", "_").replace(":", "").replace("Z", "")

def makeNewFileName(f):
    if os.path.exists(f):
        name, ext = os.path.splitext(f)
        for i in range(1, 10):
            nf = name + "(" + str(i) + ")" + ext
            if not os.path.exists(nf):
                return nf
    return f

def getMD5ofFile(f):
    h = hashlib.md5()
    with open(f) as file:
        for c in iter(lambda: file.read(4096), b""):
            h.update(c)
        return h.hexdigest()

def sortMediaFiles(path):
    global hashs, targetBase, rf

    files = []
    getFilesList(path, files)
    for f in files:
        if os.path.isdir(f):
            sortMediaFiles(f)
            continue
        if isUnsupported(f) :
            continue
        elif isPicture(f) :
            t = getImageDate(f)
            if t:
                date = str(t.tm_year) + "{:02d}".format(t.tm_mon) + "{:02d}".format(t.tm_mday) + "_" + "{:02d}".format(t.tm_hour) + "{:02d}".format(t.tm_min) + "{:02d}".format(t.tm_sec)
            else:
                print f
                continue
        elif isMovie(f) :
            t = getMovieDate(f)
            if t:
                date = t
            else:
                print f
                continue
        else :
            print f
            continue
        #md5 = getMD5ofFile(f)
        #if md5 in hashs:
        #    print "[" + f + "] is same as [" + hashs[md5] + "]"
        #else:
        #    hashs[md5] = f
        np = targetBase + "/" + date[:4] + "/" + date[4:6] + "/"
        if not os.path.exists(np):
            os.makedirs(np)
        name, ext = os.path.splitext(f)
        nf = makeNewFileName(np + date + ext.lower())
        rf.write("Move [" + f + "] to [" + nf + "]\n")

rf = open("result.txt", "w")
sortMediaFiles(basedir)
rf.close()
    
