import json
import requests
import urllib2
from helper import *
from Tkinter import *


root = Tk()
x=10
x=str(x)
print "in data.py " + x
label1 = Label(root, text='Traffic from server '+x)
label1.pack(side=LEFT, padx=5, pady=5)
label1.place(x=25, y=25)
label2 = Label(root, text='Traffic from cache '+x)
label2.pack(side=LEFT, padx=5, pady=5)
label2.place(x=25, y=75)
label1 = Label(root, text='Traffic uploaded '+x)
label1.pack(side=LEFT, padx=5, pady=5)
label1.place(x=25, y=125)
root.wm_geometry("300x300+300+300")
root.mainloop()






#req_str = 'GET_CACHE_DATA'
#ret_str = urllib2.urlopen(tracker_address + req_str).read()
