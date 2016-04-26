from time import sleep
from Tkinter import *
import PIL.Image
import PIL.ImageTk


root = Tk()
uploaded= sys.argv[1]
uploaded=str(uploaded)
print "in data.py " + uploaded
downloaded= sys.argv[2]
downloaded=str(downloaded)
print "in data.py " + downloaded
img = PIL.Image.open("black.jpg")
background_image=PIL.ImageTk.PhotoImage(img)
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.place(x=0, y=0, width=1200, height=900)
background_label.image = background_image
background_label.pack()
label1 = Label(root, text='Bytes uploaded '+uploaded)
label1.pack(side=LEFT, padx=5, pady=5)
label1.place(x=25, y=25)
label2 = Label(root, text='Bytes downloaded '+downloaded)
label2.pack(side=LEFT, padx=5, pady=5)
label2.place(x=25, y=75)
#label1 = Label(root, text='Traffic uploaded '+x)
#label1.pack(side=LEFT, padx=5, pady=5)
#label1.place(x=25, y=125)
but1 = Button(root, text='Exit', command=root.destroy)
but1.pack(side=LEFT, padx=5, pady=5)
but1.place(x=25, y=125)
root.wm_geometry("200x200+300+300")
root.mainloop()




