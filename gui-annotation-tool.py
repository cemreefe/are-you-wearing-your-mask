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

# create labels directory in case it does not exist
subprocess.run(["mkdir", "labels"])

# initialize csv string (the string for the save file)
# with column titles, image id & image class.
# the path for images will be "people_training/p<:06d id>.jpg"
csvs = "id,class\n"

# string to be displayed when help is called, or as default
manual = "a: other / s: no mask / d: mask / c: back / save"

# initialize window dimensions.
# the underscored dimensions are used to create space 
# for widgets to be implemented after the first design
w =400
w_=130
h =600
h_=0


# initialize Tkinter window
window = Tk()
window.title("Simplest Image Labeler")
window.geometry('{}x{}'.format(w+w_,h+h_))

# the labels will be saved to the csv file as numbers,
# which key should be used for which label can be found through this dictionary
labeldic = {
	"0": "s",
	"1": "d",
	"2": "a"
}

# create a canvas to display the image to be annotated
canvas = Canvas(window, width = w, height = h-150)	  
canvas.pack()	

# resizing coefficient
u=3 

# image start index
i=0

# loaded image start index
loadinit = 0

# function to remove last line from string
def rll(s):
	return s[:s.rfind('\n')]

# function to convert saved file to "labeling history" to be displayed on the right of the window
def file2hist(s):
	return s.replace(",0",": s").replace(",1",": d").replace(",2",": a")

# load an image
def loadimg(i):
	# if image exists, return image    
	try:
		img2 = Image.open("peep/p{:06d}.jpg".format(i))
		img2 = img2.resize((img2.size[0]*u, img2.size[1]*u),Image.NEAREST)
		imgtk2 = ImageTk.PhotoImage(img2) 
		return imgtk2
	# if no such image exists, this means we are out of images to label. 
	# save to a file and wait for exit command.
	except:
		timestamp = int(time.time()//1)
		f = open("labels/FINAL_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		lbl.configure(text= "Congrats! Saved to FINAL_{}.txt".format(timestamp))
		set_text("")

# load first image
imgtk = loadimg(i) 

# display image on canvas
canvas.create_image(w//2,h//2-50, anchor=CENTER, image=imgtk)	  
canvas.grid(column=0, row=2)

# add `Label` widget to display labeling history
history = Label(window, text ="<history>", anchor="s")
history.config(background='#eeeeee', relief = SUNKEN, height = 20, width = 10)
history.grid(column=2, row=2)

# display image path on a `Label` above the image
ttl = Label(window, text="peep/p{:06d}.jpg".format(i))
ttl.grid(column=0, row=1)

# empty `Label`
lbb = Label(window, text="")
lbb.grid(column=0, row=3)

# `Label` to communicate to the user
lbl = Label(window, text=manual)
lbl.grid(column=0, row=4)

# Textbox for commands from the user
txt = Entry(window,width=10)
txt.grid(column=0, row=5)
txt.focus()

# set the text of the textbox
def set_text(text):
	txt.delete(0,END)
	txt.insert(0,text)
	return

# handler for when the "submut button" is clicked
# or when <Return> or <Alt_Left> are pressed
def clicked():

	global csvs
	global imgtk
	global i
	global loadinit

    # take input as string
	imp = txt.get()

	# a: back
	if imp == "a":
		csvs += repr(i) + "," "2\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	# s: no mask
	elif imp == "s":
		csvs += repr(i) + "," "0\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	# d: mask
	elif imp == "d":
		csvs += repr(i) + "," "1\n"

		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")
		i+=1

	# c: go back
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

	# save: save current history to a file    
	elif imp == "save":
		timestamp = int(time.time()//1)
		f = open("labels/labels_{}.txt".format(timestamp),"w+")
		f.write(csvs)
		f.close()
		lbl.configure(text= "Saved to labels_{}.txt".format(timestamp))
		set_text("")

	# help: displays help text
	elif imp == "help":
		lbl.configure(text= "a: other / s: no mask / d: mask / c: back / save")
		set_text("")

	# exit: terminates the program
	elif imp == "exit":
		timestamp = int(time.time()//1)
		exit()

	# load: if no file is specified (i.e. "load last_save.txt")
	# load "labels/save.txt"
	# if file is specified, load "labels/<specified file>"
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

	# after each labeling, save to "save.txt" as a rescue save.
	# keep in mind that this save will be overwritten as soon as 
	# you enter a command other then "load" when you open up the program again
	f = open("labels/save.txt","w+")
	f.write(csvs)
	f.close()

	# update file name
	ttl.configure(text= "peep/p{:06d}.jpg".format(i))
    
	# load next image
	imgtk = loadimg(i)

	# display the loaded image
	canvas.create_image(w//2,h//2-50, anchor=CENTER, image=imgtk)
	canvas.grid(column=0, row=2)

	# update history
	history.configure(text= file2hist(csvs))

# define a callback to bind with physical keys
def callback(event):
	clicked()

# bind desired keys to the callback.
# Return key for submitting while using the tool w/ two hands
# Left Alt key for using the tool w/ one hand
window.bind('<Return>', callback)
window.bind('<Alt_L>', callback)

# display submit button
btn = Button(window, text="Submit", command=clicked)
btn.grid(column=0, row=6)

# run the gui program
window.mainloop()
