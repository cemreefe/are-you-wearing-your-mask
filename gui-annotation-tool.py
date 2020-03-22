# dependencies: 
# *pillow
# *opencv
# *tkinter

# no error handling implemented yet.

# COMMANDS:
# s:	wearing a mask
# d:	not wearing a mask
# a:	others
# save:	save to labels_<timestamp>.txt
# load	<filename>: load from labels/<filename>
# exit:	exit

# PS: everytime a label is entered, the current csvs is saved to labels/save.txt
# so that the file can be used as a recovery option. In order not to lose your recovery data, 
# directly enter the "load" command upon entering the application. 
# Any other command will result in loss of all recovery data.


import cv2
import time
import subprocess
from tkinter import *
from PIL import Image
from PIL import ImageTk


subprocess.run(["mkdir", "labels"])

csvs = "id,class\n"
manual = "a: other / s: no mask / d: mask / c: back / save"

window = Tk()

w =400
w_=130
h =600
h_=0

labeldic = {
	"0": "s",
	"1": "d",
	"2": "a"
}


window.title("Simplest Image Labeler")
window.geometry('{}x{}'.format(w+w_,h+h_))

canvas = Canvas(window, width = w, height = h-150)	  
canvas.pack()	

u=3 
i=0
loadinit = 0

#remove last line from string
def rll(s):
	return s[:s.rfind('\n')]

def file2hist(s):
	return s.replace(",0",": s").replace(",1",": d").replace(",2",": a")

def loadimg(i):
	try:
		img2 = Image.open("peep/p{:06d}.jpg".format(i))
		img2 = img2.resize((img2.size[0]*u, img2.size[1]*u),Image.NEAREST)
		imgtk2 = ImageTk.PhotoImage(img2) 
		return imgtk2
	except:
		timestamp = int(time.time()//1)
		f = open("labels/FINAL_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		lbl.configure(text= "Congrats! Saved to FINAL_{}.txt".format(timestamp))
		set_text("")


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

	global loadinit

	imp = txt.get()

	#a: back
	if imp == "a":
		csvs += repr(i) + "," "2\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#s: no mask
	elif imp == "s":
		csvs += repr(i) + "," "0\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#d: mask
	elif imp == "d":
		csvs += repr(i) + "," "1\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	#c: go back
	elif imp == "c":
		if i!=0:
			csvs = rll(rll(csvs))+"\n"

			prevlbl = labeldic[csvs.split(",")[-1][0]]
			i-=1
			print(repr(i) + " " + repr(loadinit))
			lbl.configure(text= "Label this image again. (you entered:{})".format(prevlbl))
			set_text("")
		else:
			lbl.configure(text= "Can't go back, this is the first image.")
			set_text("")

	elif imp == "save":
		timestamp = int(time.time()//1)
		f = open("labels/labels_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		lbl.configure(text= "Saved to labels_{}.txt".format(timestamp))
		set_text("")

	elif imp == "help":
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")

	elif imp == "exit":
		timestamp = int(time.time()//1)
		exit()

	elif imp[:4] == "load":

		lines, last_line, filename = "","","save.txt"

		if not len(imp.split()) == 1:
			print(imp.split())
			filename = imp.split()[1]

		with open('labels/{}'.format(filename), 'r') as s:
			csvs  = s.read()
			csvs  = csvs
			lines = csvs.splitlines()
			last_line = lines[-1]
		s.close()

		loadinit = int(last_line.split(",")[0])
		i = loadinit+1
		lbl.configure(text= "Loaded {} labels from \"{}\"".format(i-1, filename))
		set_text("")

	else:
		lbl.configure(text= manual)
		set_text("")


	f = open("labels/save.txt","w+")
	f.write(csvs)
	f.close()

	
	ttl.configure(text= "peep/p{:06d}.jpg".format(i))

	imgtk = loadimg(i)

	canvas.create_image(w//2,h//2-50, anchor=CENTER, image=imgtk)
	canvas.grid(column=0, row=2)

	history.configure(text= file2hist(csvs))

def callback(event):
	clicked()

window.bind('<Return>', callback)
window.bind('<Alt_L>', callback)



btn = Button(window, text="Submit", command=clicked)
btn.grid(column=0, row=6)





window.mainloop()
