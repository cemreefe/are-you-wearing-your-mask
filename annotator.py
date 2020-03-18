#dependencies: 
#*pillow
#*opencv
#*tkinter

import cv2
import time
from tkinter import *
from PIL import Image
from PIL import ImageTk


csvs = ""
manual = "a: other / s: no mask / d: mask / c: back / save"

window = Tk()

w =400
w_=130
h =600
h_=0

labels = []

window.title("Simplest Image Labeler")
window.geometry('{}x{}'.format(w+w_,h+h_))

canvas = Canvas(window, width = w, height = h-150)	  
canvas.pack()	

u=3 
i=0 

def loadimg(i):
	img2 = Image.open("peep/p{:06d}.jpg".format(i))
	img2 = img2.resize((img2.size[0]*u, img2.size[1]*u),Image.NEAREST)
	imgtk2 = ImageTk.PhotoImage(img2) 
	return imgtk2

imgtk = loadimg(i) 


canvas.create_image(w//2,h//2-50, anchor=CENTER, image=imgtk)	  
canvas.grid(column=0, row=2)

history = Label(window, text ="<history>", anchor="s")
history.config(background='#eeeeee', relief = SUNKEN, height = 20, width = 10)
history.grid(column=2, row=2)

ttl = Label(window, text="peep/p{:06d}.jpg".format(i))
ttl.grid(column=0, row=1)


lbb = Label(window, text="")
lbb.grid(column=0, row=3)

lbl = Label(window, text=manual)
lbl.grid(column=0, row=4)

txt = Entry(window,width=10)
txt.grid(column=0, row=5)
txt.focus()

def set_text(text):
	txt.delete(0,END)
	txt.insert(0,text)
	return


def clicked():

	global csvs
	global imgtk
	global i
	global labels

	imp = txt.get()

	#a: back
	if imp == "a":
		csvs += repr(i) + ",	" "2\n"
		labels.append(imp)
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#s: no mask
	elif imp == "s":
		csvs += repr(i) + ",	" "0\n"
		labels.append(imp)
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#d: mask
	elif imp == "d":
		csvs += repr(i) + ",	" "1\n"
		labels.append(imp)
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#c: go back
	elif imp == "c":
		if i!=0:
			csvs = csvs[:csvs.rfind("\n")+1]
			labels = labels[:-1]
			i-=1
			lbl.configure(text= "Label this image again. (you entered:{})".format(labels[i-1]))
			set_text("")
		else:
			lbl.configure(text= "Can't go back, this is the first image.")
			set_text("")

	elif imp == "save":
		timestamp = int(time.time()//1)
		f = open("labels_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		lbl.configure(text= "Saved to labels_{}.txt".format(timestamp))
		set_text("")

	elif imp == "help":
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")

	elif imp == "exit":
		timestamp = int(time.time()//1)
		f = open("labels_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		exit()

	else:
		lbl.configure(text= manual)
		set_text("")


	f = open("save.txt","w+")
	f.write(csvs)
	f.close()

	
	ttl.configure(text= "peep/p{:06d}.jpg".format(i))

	imgtk = loadimg(i)

	canvas.create_image(w//2,h//2-50, anchor=CENTER, image=imgtk)
	canvas.grid(column=0, row=2)

	history.configure(text= csvs.replace(",	0",": s").replace(",	1",": d").replace(",	2",": a"))

def callback(event):
	clicked()

window.bind('<Return>', callback)



btn = Button(window, text="Submit", command=clicked)
btn.grid(column=0, row=6)





window.mainloop()
