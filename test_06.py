from tkinter import *
from tkinter.messagebox import showinfo
import win32api
import win32con

def reply():
    #showinfo(title="Reply", message = "Hello %s!" % name)
    win32api.keybd_event(9, 0, 0, 0)
    win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)


top = Tk()
top.title("Echo")
#top.iconbitmap("Iconshock-Folder-Gallery.ico")

Label(top, text="Enter your name:").pack(side=TOP)
ent = Entry(top)
ent.bind("<Return>", (lambda event: reply()))
ent.pack(side=TOP)
ent1 = Entry(top)
ent1.bind("<Return>", (lambda event: reply()))
ent1.pack(side=TOP)
ent2 = Entry(top)
ent2.bind("<Return>", (lambda event: reply()))
ent2.pack(side=TOP)
btn = Button(top,text="Submit", command=(lambda: reply()))
btn.pack(side=LEFT)

top.mainloop()