#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlink
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import subprocess
import imagehash
import glob, os
from PIL import Image
from streamlink import Streamlink


# In[ ]:

duration = int(sys.argv[1]) if len(sys.argv) >= 2 else 3600

print("Person detector will work for {} minutes.".format(duration//60))


possible_duplicates = {}

class dupinstance:
    def __init__(self, img):
        self.img   = img
        self.birth = time.time()


# In[ ]:


# misc functions

def cv2resize(img, scale_percent):
    
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    return resized


def compare(enum, im1, im2):
    
    nim2 = cv2.resize(im2, (im1.shape[1],im1.shape[0]))
    im_v = cv2.hconcat([im1, nim2])
    
    diff_ = np.sum(np.square(nim2-im1))/(im1.shape[0]*im1.shape[2])
    diff  = imagehash.average_hash(Image.fromarray(nim2))-imagehash.average_hash(Image.fromarray(im1))
    
    if diff_ < 6400 and diff < 15:
        return "similar"
    elif diff_ < 6900 and diff < 21:
        return "ambigous"
    else:
        return "different"
    
    
def taxi_score(img, threshold = 500):

    taxi_color = [12,196,214]
    
    ycount  = 0
    wcount  = 0
    color_y = np.ones(img.shape)*taxi_color
    color_w = np.ones(img.shape)*255

    for row in range (img.shape[0]):
        for col in range (img.shape[1]):
            if np.mean(np.square(img[row, col] - color_y[row, col])) < threshold:
                ycount+=1

    return [ycount, wcount]


# In[4]:


input_stream = "istiklal2"

if input_stream == "istiklal1":
    input_url = "https://livestream.ibb.gov.tr/ibb_live/istiklalcadhq.stream/Playlist.m3u8"
elif input_stream == "istiklal2":
    input_url = "https://livestream.ibb.gov.tr/ibb_live/istiklalcad2hq.stream/Playlist.m3u8"
elif input_stream == "misircarsisi":
    input_url = "https://livestream.ibb.gov.tr/ibb_live/misircarsisihq.stream/chunklist_w289409329.m3u8"


# In[ ]:


session = Streamlink()

session.set_option("http-ssl-verify", False)

streams = session.streams(input_url)
stream = streams["worst"]

# In[ ]:


cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(stream.url)

# the output will be written to output.avi
#out_md = cv2.VideoWriter(
#    'media/output.avi',
#    cv2.VideoWriter_fourcc(*'MJPG'),
#    15.,
#    (640,480))

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

to_be_deleted_dc = []


FNULL = open(os.devnull, 'w')

subprocess.run(["mkdir", "people"])
timestr = time.strftime("%Y%m%d")
os.chdir("people/")
subprocess.run(["mkdir", timestr], stdout=FNULL, stderr=subprocess.STDOUT)
os.chdir(timestr + "/")
pnum = 0
tdy_imgs = os.listdir()
tdy_imgs.sort()

if len(tdy_imgs) > 0:
    pnum = int(tdy_imgs[-1][-10:-4])+1
os.chdir("../../")

enum = pnum

start_time = time.time()
elapsedminutes = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    try:
        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        if not frame.size:
            print("ERROR: Missing frame.")
            continue
    except:
        continue

    if input_stream.startswith("istiklal"):
        # crop top half if using an istiklal stream,
        # otherwise it detects windows as people
        crop_frame = frame[240:480, 0:640]
        frame = crop_frame

    # make a clean copy of the frame (cv2 images are copied by reference)
    frame_clean = frame.copy()

    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:

        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 255), 2)

        #get contents of the bounding box
        box = frame_clean[yA:yB, xA:xB]
        
        #how much does this image contain the color of a taxi?
        #this is an attempt to get rid of many yellow taxis that get recognized as people
        taximeter = taxi_score(box, 630)[0]
        litemeter = taxi_score(box, 630)[1]
        if taximeter > 160:
            continue


        isUnique   = True #until proven not
        isAmbigous = False

        #iterate through the dictionary containing possible duplicates.   
        for key, item in possible_duplicates.items():

            #if duplicate candidate is 2 minutes old, schedule to delete it (can't change dic size during iteration).
            if time.time()-item.birth > 30:
                    to_be_deleted_dc.append(key)
                    
        #iterate through the dictionary containing possible duplicates.   
        for key, item in possible_duplicates.items():

            #if the new box is already in duplicates, don't save it as a unique person.
            similarity = compare(enum, box, item.img)
            if(similarity == "similar"):
                #instead update the duplicate candidate with its newer version.
                possible_duplicates[key] = dupinstance(box)
                isUnique = False
                continue
                
            elif(similarity == "ambigous"):
                isAmbigous = True
                isUnique = False


        # delete old dcs
        for key in to_be_deleted_dc:
            if(key in possible_duplicates.keys()):
                del possible_duplicates[key]

        to_be_deleted_dc.clear()
        

        # if its unique, save it as a unique person.
        if isUnique:

            if timestr != time.strftime("%Y%m%d"):
                timestr = time.strftime("%Y%m%d")
                pnum = 0
                enum = 0
                os.chdir("people/")
                errcode = subprocess.run(["mkdir", timestr], stdout=FNULL, stderr=subprocess.STDOUT)
                os.chdir("../")
            
            cv2.imwrite("people/{}/p-{}-{:06d}.jpg".format(timestr, timestr, pnum), box)
            
            print("people/{}/p-{}-{:06d}.jpg".format(timestr,timestr, pnum))
            
            possible_duplicates[enum] = dupinstance(box)
            enum+=1
            pnum+=1
        
        if isAmbigous:
            #instead update the duplicate candidate with its newer version.
            possible_duplicates[enum] = dupinstance(box)
            enum += 1

    # Write the output video 
    # out_md.write(frame.astype('uint8'))
    #out_cl.write(frame_clean.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('mask-detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

    if elapsedminutes != (time.time() - start_time) // 60:
        elapsedminutes = (time.time() - start_time) // 60
        print("{}/{} MINS".format(int(elapsedminutes), duration//60))
    
    if time.time() - start_time > duration:
        break

print("Terminating session.")            

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)


# In[ ]:




