import os
import mimetypes
import datetime
import shutil
import PIL
from PIL import Image
from PIL.ExifTags import TAGS

Source_directory      = 'E:\\Source\\p1'
Destination_directory = 'E:\\out'


def seek_directory(d):
    found = []
    for root, dirs, files in os.walk(d):
        str(dirs)
        for f in files:
            mime = mimetypes.guess_type(f)
            if(mime[0] == 'image/jpeg'):
                found.append([mime[0], os.path.join(root, f)]) 
            elif mime[0] == 'image/png':
                found.append([mime[0], os.path.join(root, f)])               
    
    return found

def get_exif_date(f):
    r = ''
    try:
        img = Image.open(f)
    except PIL.UnidentifiedImageError:
        return r

    exif = img._getexif()
    
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'DateTimeOriginal':
           r = value

    return r

def get_ctime(f):
    return datetime.datetime.fromtimestamp(os.path.getctime(f))

if __name__ == '__main__':
    files = seek_directory(Source_directory)
    cnt = cnt_max = len(files)

    for f in files:
        ftime = ''
        if f[0] == 'image/jpeg':
            try:
                ftime = str(get_exif_date(f[1]))
            except AttributeError:
                ftime = str(get_ctime(f[1]))
            except OSError:
                ftime = str(get_ctime(f[1]))
        elif f[0] == 'image/png':
            ftime = str(get_ctime(f[1]))
    
        if ftime == '':
            ftime = str(get_ctime(f[1]))

        yyyy = ftime[0:4]
        mm   = ftime[5:7]
        t_d = Destination_directory + '\\' + yyyy + '\\' + yyyy + '-' + mm
        
        #print(yyyy + '-' + mm, end="\t")
        #print(ftime, end="\t")
        #print(type(ftime), end="\t")
        print(str(cnt) + '/' + str(cnt_max), end="\t")
        #print(f[0], end="\t")
        print(t_d, end="\t")
        print(f[0], end="\t")
        print(f[1])

        try:
            os.makedirs(t_d, exist_ok=True)
            shutil.copy2(f[1], t_d)
            #shutil.move(f, t_d + '\\' + os.path.basename(f))
        except PermissionError:
            next

        cnt -= 1
 
        
