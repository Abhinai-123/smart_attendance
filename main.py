import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import tkinter as tk
import time
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"",
    'storageBucket':""
})
bucket = storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
imgbackground=cv2.imread('resources/background.png')
folderpath='resources/Modes'
modepathlist=os.listdir(folderpath)
imgl=[]
for p in modepathlist:
    imgl.append(cv2.imread(os.path.join(folderpath,p)))
file=open('EncodeFile.p','rb')
encodelistwithnames=pickle.load(file)
file.close()
encodelistknown,memberid=encodelistwithnames
id=0
modetype=0
count = 0
while True:

    success, img=cap.read()
    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs= cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
    facecurframe=face_recognition.face_locations(imgs)
    encodecurframe=face_recognition.face_encodings(imgs,facecurframe)
    imgbackground[162:162+480,55:55+640]=img
    imgbackground[44:44 + 633, 808:808 + 414] = imgl[modetype]
    for encodeface,faceloc in zip(encodecurframe,facecurframe):
        matches=face_recognition.compare_faces(encodelistknown,encodeface)
        facedis=face_recognition.face_distance(encodelistknown,encodeface)
        matchindex=np.argmin(facedis)
        print("matches",matches)
        print("facedis",facedis)
        if matches[matchindex]:
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            id=memberid[matchindex]
            imgbackground = cvzone.cornerRect(imgbackground, bbox)
            if count == 0:
                modeType = 1
                count = 1






    if(count!=0):
    
        if(count==1):
            studentinfo=db.reference(f'Students/{id}').get()
            datetimeObject = datetime.strptime(studentinfo['last_attendance'], "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject)
            minutes=abs(int(secondsElapsed.total_seconds()//60))
            print(minutes)
            if(minutes>45):
                ref = db.reference(f'Students/{id}')
                studentinfo['attendace'] += 1
                ref.child('attendace').set(studentinfo['attendace'])
                ref.child('last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                modetype=0
            elif(minutes<45):
                modetype=3
                count=0
                imgbackground[44:44 + 633, 808:808 + 414] = imgl[modetype]
        if(modetype!=3):
                if(40<count<50):
                    modetype=2
                imgbackground[44:44 + 633, 808:808 + 414] = imgl[modetype]

                if(count<40):
                        modetype=1
                        cv2.putText(imgbackground, str(studentinfo['attendace']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(studentinfo['branch']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(studentinfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100),
                                    1)
                        cv2.putText(imgbackground, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        (w, h), _ = cv2.getTextSize(studentinfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgbackground, str(studentinfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                        print("mofkf")





        count=count+1
        if(count>50):
                modetype=0
                count=0
                imgbackground[44:44 + 633, 808:808 + 414] = imgl[modetype]


    cv2.imshow("hi", imgbackground)
    cv2.waitKey(1)


