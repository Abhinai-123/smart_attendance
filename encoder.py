import cv2
import numpy as np
from matplotlib import pyplot as plt
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import tkinter as tk
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"",
    'storageBucket':""
})
imgbackground=cv2.imread('resources/background.png')
folderpath='images'
modepathlist=os.listdir(folderpath)
imgl=[]
memberslist=[]
for p in modepathlist:
    imgl.append(cv2.imread(os.path.join(folderpath,p)))
    memberslist.append(os.path.splitext(p)[0])
    filename=f'{folderpath}/{p}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)


def encoder(imglist):
    encodelist=[]
    for img in imglist:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("pathfound")
print("Encoding finished")
encodelistknown=encoder(imgl)
encodelistwithnames=[encodelistknown,memberslist]
file=open("EncodeFile.p",'wb')
pickle.dump(encodelistwithnames,file)
file.close()