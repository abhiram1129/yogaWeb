from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from suryaNamCpy import detectPose, poseAngles, calculateAngle, mp_pose, pose, mp_drawing, pose_video, asanaInventory, asanaName, percentageMeter, accuracyMeter, bodyAngles, duration, x
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import math
import cv2
import numpy as np
from time import perf_counter, time
import mediapipe as mp
import matplotlib.pyplot as plt
from playsound import playsound


# Create your views here.

def index(request):
    return render(request, 'index.html')

def start(request):
    return render(request, 'start.html')

#def suryanamaskar(request):
    #return StreamingHttpResponse(suryaNamaskaram())
    # return render(request, 'suryanamaskar.html')

def suryanamaskar(request):
    return render(request, 'suryanamaskar.html')


@gzip.gzip_page
def Home(request):
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")


#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.duration = 0
        self.x=0
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
        while self.video.isOpened():
            
            (self.grabbed, self.frame) = self.video.read()
            self.frame = cv2.flip(self.frame, 1)
            self.frame, landmarks = detectPose(self.frame, pose_video, display=False)
            if landmarks:
                self.frame, _ = poseAngles(landmarks, self.frame)
                j=0
                sumValue = 0
                # x=0
                name = asanaName[self.x]
                
                cv2.rectangle(self.frame, (0,0),(650,50),(0,0,0),-1)
                cv2.putText(self.frame, "{}". format(name) , (10, 40),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                asana = asanaInventory[self.x]
                for i in bodyAngles :
                    percentage=percentageMeter(i,asana[j])
                    sumValue = sumValue + percentage
                    j=j+1
                avg = round(sumValue/8,2)
            
                if avg >= 85:
                    self.duration = self.duration + 1 
                else: 
                    while self.duration >0:
                        self.duration = self.duration - 1
                #print(duration)
                #print(m)
                if self.duration > 5 and self.duration <= 35:
                        cv2.putText(self.frame, "Hold your pose" , (100, 200),cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
                        if self.duration%10==0:
                            playsound('audio/clockcut.wav', False)                    
                if self.duration > 35 and self.duration <= 39:
                        cv2.putText(self.frame, "Good job :)" , (100, 200),cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
                        if self.duration == 39:
                            playsound('audio/win.wav', False)
                if self.duration > 60 :
                    self.x=self.x+1
                    self.duration=0
                #print(x)
                
                #print(self.duration)
                
                cv2.putText(self.frame, "Accuracy : {}".format(avg) , (400, 40),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                accuracyScore = accuracyMeter(avg, self.frame)
                #cv2.putText(frame, "Level : {}".format(accuracyScore) , (50, 90),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                #plt.imshow(frame, meter)
            
            sumValue = 0

            image = self.frame
            _, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')