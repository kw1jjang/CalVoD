import threading
from ftpclient import runrecv

class Requester(threading.Thread, object):
    def __init__(self, user="user", pw="1"):
        self.user = user
        self.pw = pw
        threading.Thread.__init__(self)
        print "User: " + self.user + ", " + self.pw

    def run(self):
       runrecv(self.user, self.pw)
        

def run_threads(num):
    thread_list = [0]*num
    for ref in range(num):
        thread_list[ref] = Requester("user" + str(ref + 1), str(ref+1))
    for ref in range(num):
        thread_list[ref].start()


if __name__ == "__main__":
    run_threads(3)
