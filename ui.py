"""
Created on Fri Mar  4 12:30:46 2016

@author: alagu
"""
#TK GUI for desktop applications

from Tkinter import *
import tkMessageBox as tm
import PIL.Image
import PIL.ImageTk
import os
import urllib2
from helper import *


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
    
        
        self.img = PIL.Image.open("pic.jpg")
        self.background_image=PIL.ImageTk.PhotoImage(self.img)
        self.background_label = Label(self, image=self.background_image)
	#self.background_label = Label(self, bg="white")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = self.background_image
        self.background_label.pack()
        self.pack()
        
        
        self.label_1 = Label(self, text="Username")
        self.label_1.place(x=100, y=10)
        self.label_2 = Label(self, text="Password")
        self.label_2.place(x=100, y=60)
                             
        self.entry_1 = Entry(self)
        self.entry_1.place(x=200, y=10)
        self.entry_2 = Entry(self, show="*")
        self.entry_2.place(x=200, y=60)
                             
                            
        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.place(x=100, y=120)
                             
        self.logbtn = Button(self, text="Login", command = self._login_btn_clickked)
        self.logbtn.place(x=100, y=180)
                             
        self.pack()
    
    def _login_btn_clickked(self):

	logged_in = False;
	while(logged_in == False):
  		username = self.entry_1.get()
        	password = self.entry_2.get()
		print username
  		req_str = 'VERIFY_ACCOUNT&' + username + '_' + password
		tracker_address = load_tracker_address()
  		print 'request sent to tracker: ' + tracker_address + req_str
  		ret_str = urllib2.urlopen(tracker_address + req_str).read()
		print ret_str
		print "ABCDEFGHIJ"
  		if ret_str == 'True':
    			logged_in = True
			#tm.showinfo("Login info", "Welcome")
			self.quit()
			root3 = Toplevel()
    			main3 = MainView3(root3, username, password)
    			main3.pack(side="top", fill="both", expand=True)
    			root3.wm_geometry("720x580+300+300")
    			root3.mainloop()
			self.destroy()

    #bandwidth = main.p3.set_badwidth()
    #storage = main.p3.set_storage()
			


        	else:
            		tm.showerror("Login error", "The username and password do not match")

class Page3(Page):
    def __init__(self, root, username, password):
        Page.__init__(self, root)
	self.username = "chen"
	self.password = "11111"
    
        
        self.img = PIL.Image.open("pic.jpg")
        self.background_image=PIL.ImageTk.PhotoImage(self.img)
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = self.background_image
        self.background_label.pack()
        self.pack()
        
        
        self.label_1 = Label(self, text="Please select the amount of resources you are willing to contribute:")
        self.label_1.place(x=100, y=10)
	self.range=[("Minimum",1),("Half",2),("Maximum",3)]
	self.s=IntVar()
	self.s.set(0)
	space=0
	for text,mode in self.range:
		b=Radiobutton(self,text=text,variable=self.s,command=self.set_bandwidth,value=mode)
		b.place(x=100, y=50+space)
		space=space+50
        

	'''self.label_2 = Label(self, text="Choose amount of storage:")
        self.label_2.place(x=100, y=250)
	self.range2=[("None",1),("0-25%",2),("26-50%",3),("51-75%",4),("76-100%",5)]
	self.t=IntVar()
	self.t.set(0)
	space2=0
	for text2,mode2 in self.range2:
		b2=Radiobutton(self,text=text2,variable=self.t,command=self.set_storage,value=mode2)
		b2.place(x=100, y=10+space)
		space2=space2+50'''
        self.btn = Button(self, text="Enter", command = self.btn_clickked)
        self.btn.place(x=100, y=300)
                             
        self.pack()

    def set_bandwidth(self):
	self.bandwidth = self.s.get()
	
    def set_storage(self):
	self.storage = self.t.get()

    def get_bandwidth(self):
	return self.bandwidth
	
    def get_storage(self):
	return self.storage

    def btn_clickked(self):
	cache_options = ['0.25', '0.5', '1']
	cache_multiplier = cache_options[self.bandwidth - 1]
	os.system('./populate_caches_local_ui.sh ' + cache_multiplier + ' ' + self.username + ' ' + self.password)
	print "alagu debug"
	os.system('./populate_user_ui.sh ' + self.username + ' ' + self.password)
        self.quit()
        self.destroy()

class MainView3(Frame):
    def __init__(self, root, username, password):
        Frame.__init__(self, root)
	self.username = username
	self.password = password
        self.p3 = Page3(self, self.username, self.password)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b3 = Button(buttonframe, text="Cache Settings", command=self.p3.lift)
       
        b3.pack(side="left")
	self.p3.show()

class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
    
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Home", command=p1.lift)
        b1.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("720x580+300+300")
    root.mainloop()
