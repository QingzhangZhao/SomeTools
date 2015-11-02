import requests
import sys
import os 
import time

url=sys.argv[1]


def get_filesize_and_filename(url):
    re = requests.get(url)
    filesize = re.headers['Content-Length']
    if 'filename' in re.headers:
        filename=re.headers['filename']
    else:
        filename=None
    return (re,int(filesize),filename)


def is_support_continue(url):
    header_range={
                   'Range':'bytes=0-'
    }
    re = requests.get(url,headers=header_range)
    if 'Content-Range' in re.headers:
        return True
    else:
        return False


def  simple_download(re,filename,headers={},cookies={}):
    file = open(filename,'wb')
    try:
        print ("-----Start DownLoading-----")
        for block in re.iter_content(chunk_size=1024):

            file.write(block)
            time.sleep(1)
            file.flush()
        file.close()
    except:
        print ("Pause!")
        exit(-1)
    print ("-----Successfully Downloaded!-----")


def download_with_continue(url,filename='',headers={},cookies={}):
    re,filesize,filename=get_filesize_and_filename(url)
    if filename is None:
        filename=url.split('/')[-1]
    if os.path.exists(filename):
        current_size = os.path.getsize(filename)
        if current_size < filesize:
            head = {'Range':'bytes=%d-'%(current_size)}
            file = open(filename,"ab+")
            text = requests.get(url,headers=head)
            for block in text.iter_content(chunk_size=1024):
                file.write(block)
                file.flush() 
                progress=int((os.path.getsize(filename)/filesize)*100)
                sys.stdout.write('\b'*102+'['+'#'*progress+' '*(100-progress)+']')
                time.sleep(0.01)
                sys.stdout.flush()
            print ("---Finshed!---")
            file.close()
        else:
            print ("The file already exists!")
    else:
        simple_download(re,filename,headers,cookies)

download_with_continue(url)
