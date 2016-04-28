from time import sleep
from Tkinter import *
import PIL.Image
import PIL.ImageTk


root = Tk()
uploaded_server= sys.argv[1]
uploaded_server=str(uploaded_server)
uploaded_cache= sys.argv[2]
uploaded_cache=str(uploaded_cache)
print "in data.py server " + uploaded_server
print "in data.py cache " + uploaded_cache
downloaded_server= sys.argv[3]
downloaded_server=str(downloaded_server)
downloaded_cache= sys.argv[4]
downloaded_cache=str(downloaded_cache)
print "in data.py server" + downloaded_server
print "in data.py cache" + downloaded_cache
img = PIL.Image.open("black.jpg")
background_image=PIL.ImageTk.PhotoImage(img)
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.place(x=0, y=0, width=1200, height=900)
background_label.image = background_image
background_label.pack()
label1 = Label(root, text='Bytes downloaded from server: '+ downloaded_server)
label1.pack(side=LEFT, padx=5, pady=5)
label1.place(x=25, y=25)
label2 = Label(root, text='Bytes downloaded from caches: '+ downloaded_cache)
label2.pack(side=LEFT, padx=5, pady=5)
label2.place(x=25, y=50)
label1 = Label(root, text='Bytes uploaded to server: '+ uploaded_server)
label1.pack(side=LEFT, padx=5, pady=5)
label1.place(x=25, y=100)
label2 = Label(root, text='Bytes uploaded to caches: '+ uploaded_cache)
label2.pack(side=LEFT, padx=5, pady=5)
label2.place(x=25, y=125)
#label1 = Label(root, text='Traffic uploaded '+x)
#label1.pack(side=LEFT, padx=5, pady=5)
#label1.place(x=25, y=125)
but1 = Button(root, text='Exit', command=root.destroy)
but1.pack(side=LEFT, padx=5, pady=5)
but1.place(x=25, y=175)
root.wm_geometry("300x300+300+300")
root.mainloop()




