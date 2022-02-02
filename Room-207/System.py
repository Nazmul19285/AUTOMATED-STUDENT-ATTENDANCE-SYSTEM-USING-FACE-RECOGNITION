import face_recognition as fr
import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from datetime import datetime
import pandas as pd
import csv
import numpy as np


while(True):
    def encode_faces(folder):
        list_people_encoding = []

        for filename in os.listdir(folder):
            known_images = fr.load_image_file(f'{folder}{filename}')
            konwn_encodings = fr.face_encodings(known_images)[0]
            list_people_encoding.append((konwn_encodings, filename))

        return list_people_encoding


    def markAttendance(name):
        atendanceSheet = pd.read_csv(atendancePath)
        students = atendanceSheet.iloc[:,0].values

        with open(atendancePath) as ap:
            h = ap.readline()
        classDates = h.split(",")

        c = 0
        for x in classDates:
            c += 1
        
        c = 10/c


        dateCounter = 0
        for x in classDates:
            if(x.rstrip() == todayDate.rstrip()):
                break
            dateCounter += 1

        j = -1
        for x in classDates:
            j += 1
            
        y = 1
        for x in students:
            if(name == x):
                r = csv.reader(open(atendancePath))
                lines = list(r)
                if(lines[y][dateCounter] == '0'):
                    lines[y][dateCounter] = '1'
                    lines[y][j] = str(float(lines[y][j])+c)
                    writer = csv.writer(open(atendancePath, 'w'))
                    writer.writerows(lines)
            y += 1


    def find_target_faces():
        face_location = fr.face_locations(target_image)
        for person in encode_faces(path):
            encoded_face = person[0]
            filename =person[1]

            try:
                is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.5)
                print(f'{is_target_face} {filename}')
            except Exception:
                print("no face found")
            

            if face_location:
                face_number = 0
                for location in face_location:
                    if is_target_face[face_number]:
                        label = os.path.splitext(filename)[0]
                        label = str(label)
                        label = label.split("-")
                        print(label[0])
                        create_fram(location, label[0])

                        markAttendance(label[0])

                    face_number +=1




    def create_fram(location, label):
        top, right, bottom, left = location

        cv.rectangle(target_image, (left,top), (right, bottom), (255,0,0), 2)
        cv.rectangle(target_image, (left,bottom + 20), (right, bottom), (255,0,0), cv.FILLED)
        cv.putText(target_image, label, (left + 3, bottom + 14), cv.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1)


    def render_image():
        rgb_img = cv.cvtColor(target_image, cv.COLOR_BGR2RGB)
        cv.imshow('Face Recognition', rgb_img)
        cv.waitKey(10)


    with open('ClassRoutine.csv') as f:
        classTimes = f.readline()
    classTimes = classTimes.split(",")

    Routine = pd.read_csv("ClassRoutine.csv")
    days = Routine.iloc[:,0].values

    today= datetime.now()
    today = today.strftime("%A")
    #print(today)

    todayDate = datetime.date(datetime.now())
    todayDate = todayDate.strftime("%d %b %Y")

    '''Tk().withdraw()
    load_image = askopenfilename()
    target_image = fr.load_image_file(load_image)'''

    video_capture = cv.VideoCapture(0)
    while (True):
        ret, frame = video_capture.read()
        frame = cv.resize(frame, (1000, 800))
        cv.imshow("Frame", frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
        #break
    video_capture.release()
    cv.destroyAllWindows()

    target_image = frame
    target_encoding = fr.face_encodings(target_image)

    path = None
    atendancePath = None
    students = []
    rowCounter = 0

    for x in days:
        if(x.rstrip() == today.rstrip()):
            classes = Routine.iloc[rowCounter,:].values
            classes = np.delete(classes, 0)
            durationCounter = 1
            for y in classes:
                duration = classTimes[durationCounter]
                startTime, endTime = duration.split("-")

                current_time = datetime.now()
                current_time = current_time.strftime("%H:%M")

                if(current_time >= startTime) and (current_time < endTime):
                    if(y == "CSE_101"):
                        path = "CSE_101/Students/"
                        atendancePath = "CSE_101/CSE_101.csv"
                    elif(y == "CSE_302"):
                        path = "CSE_302/Students/"
                        atendancePath = "CSE_302/CSE_302.csv"
                    elif(y == "CSE_312"):
                        path = "CSE_312/Students/"
                        atendancePath = "CSE_312/CSE_312.csv"

                durationCounter += 1

        rowCounter +=1
        #print(path,atendancePath)

    find_target_faces()
    render_image()
