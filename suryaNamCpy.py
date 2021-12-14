import math
import cv2
import numpy as np
from time import perf_counter, time
import mediapipe as mp
import matplotlib.pyplot as plt
from playsound import playsound

def calculateAngle(landmark1, landmark2, landmark3):

      x1, y1, _ = landmark1
      x2, y2, _ = landmark2
      x3, y3, _ = landmark3
  
      angle = round(math.degrees(math.atan2(y3 - y2, x3 - x2) 
      - math.atan2(y1 - y2, x1 - x2)),2)
      if angle < 0:
          angle += 360
      
      if angle > 180:
        angle = 360 - angle 

      return angle

def detectPose(image, pose, display=True):
      
      output_image = image.copy()
      imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(imageRGB)
      height, width, _ = image.shape
      landmarks = []
      
      if results.pose_landmarks:
          mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS)
          for landmark in results.pose_landmarks.landmark:
              landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                    (landmark.z * width)))
      
      if display:
          
          plt.figure(figsize=[12,12])
          plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
          plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
          
          mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

      else:        
          return output_image, landmarks

def poseAngles(landmarks, output_image):    

      # left shoulder, elbow and wrist
      bodyAngles[0] = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
      
      # right shoulder, elbow and wrist 
      bodyAngles[1] = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
      
      # left elbow, shoulder and hip 
      bodyAngles[2] = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
  
      # right hip, shoulder and elbow 
      bodyAngles[3] = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
  
      #left hip, knee and ankle  
      bodyAngles[4] = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
  
      #right hip, knee and ankle 
      bodyAngles[5] = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

      bodyAngles[7] = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

      bodyAngles[6] = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
      
      #print(bodyAngles)
      return (output_image, bodyAngles)

def percentageMeter(userAngle,expectedAngle):
          #print(userAngle)
          
          if userAngle>expectedAngle:
            percentage = round((expectedAngle/userAngle)*100,2)
          else:    
            percentage = round((userAngle/expectedAngle)*100,2)
          
          return(percentage)

def accuracyMeter(finalVal, frameName):

          if(finalVal<=25):
            accuracy="poor"
            cv2.rectangle(frameName, (20,70),(620,460),(0,0,255),20)
          elif(finalVal>25 and finalVal<=50):
            accuracy="decent"
            cv2.rectangle(frameName, (20,70),(620,460),(0,128,255),20)          
          elif(finalVal>50 and finalVal<=75):
            accuracy="good" 
            cv2.rectangle(frameName, (20,70),(620,460),(0,255,255),20)
          elif(finalVal>75 and finalVal<=80):
            accuracy="very good"
            cv2.rectangle(frameName, (20,70),(620,460),(0,255,255),20)  
          elif(finalVal>80):
            accuracy="perfect"
            cv2.rectangle(frameName, (10,70),(620,460),(0,255,0),20)
          
          return(accuracy)


  

      # Calculate the required angles.

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

# Initialize the VideoCapture object to read from the webcam.
#camera_video = cv2.VideoCapture(0)

# Initialize a resizable window.
#cv2.namedWindow('Pose Classification', cv2.WINDOW_NORMAL)

asanaInventory = np.empty(12, dtype='object')

asanaInventory[0] = np.array([56,56,30,30,180,180,175,175])
asanaInventory[1] = np.array([170,170,160,160,180,180,140,140])
asanaInventory[2] = np.array([165,165,120,120,175,175,30,30])
asanaInventory[3]= np.array([170,170,30,30,30,135,40,130])
asanaInventory[4] = np.array([175,175,70,70,170,170,175,175])
asanaInventory[5] = np.array([35,35,25,25,140,140,145,145])
asanaInventory[6] = np.array([85,85,5,5,180,180,145,145])
asanaInventory[7] = np.array([175,175,175,175,175,175,85,85])
asanaInventory[8]= np.array([170,170,30,30,145,30,140,40])
asanaInventory[9] = np.array([165,165,120,120,175,175,30,30])
asanaInventory[10] = np.array([170,170,160,160,180,180,140,140])
asanaInventory[11] = np.array([56,56,30,30,180,180,175,175])

asanaName = (["Pranamasana"],["Hasthauttanasasana"],["Hasthapadasana"],["Ashwa Sanchalanasana"],["Dandasana"],["Ashtanga Nmaskara"],["Bhujangasan"],["Adho Mukha Shwanasana"],["Hasthapadasana"],["Hasthauttanasana"],["Pranamasana"])

bodyAngles = np.empty(8, dtype='object')
duration = 0.0
x=0

# Iterate until the webcam is accessed successfully.
# while camera_video.isOpened():
#     ok, frame = camera_video.read()
#     if not ok:        
#         continue
#     # Flip the frame horizontally for natural (selfie-view) visualization.
#     frame = cv2.flip(frame, 1)
#     frame_height, frame_width, _ =  frame.shape
#     frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
#     frame, landmarks = detectPose(frame, pose_video, display=False)
#     #duration=0
#     #x=0
#     if landmarks:
#         frame, _ = poseAngles(landmarks, frame)
#         #x=0
#         j=0
#         sumValue = 0
#         #x=0
#         name = asanaName[x]
        
#         cv2.rectangle(frame, (0,0),(900,100),(0,0,0),-1)
#         cv2.putText(frame, "{}". format(name) , (400, 70),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
#         #plt.imshow(pic[:,:,::-1]);plt.title("Sample Image");plt.axis('off');plt.show()

#         asana = asanaInventory[x]
#         for i in bodyAngles :
#             percentage=percentageMeter(i,asana[j])
#             sumValue = sumValue + percentage
#             j=j+1
#         avg = round(sumValue/8,2)
    
#         if avg >= 85:
#             duration = duration + 1 
#         else: 
#             while duration >0:
#                 duration = duration - 1
#         #print(duration)
#         #print(m)
#         if duration > 5 and duration <= 15:
#                 cv2.putText(frame, "Hold your pose" , (150, 600),cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
#                 if duration%10==0:
#                   playsound('audio/clockcut.wav', False)                    
#         if duration > 15 and duration <= 18:
#                 cv2.putText(frame, "Good job :)" , (150, 600),cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
#                 if duration == 17:
#                     playsound('audio/win.wav', False)
#         if duration > 18 :
#             x=x+1
#             duration=0
#         #print(x)
        
#         #print(duration)
        
#         cv2.putText(frame, "Accuracy : {}".format(avg) , (20, 70),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         accuracyScore = accuracyMeter(avg, frame)
#         #cv2.putText(frame, "Level : {}".format(accuracyScore) , (50, 90),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
#         #plt.imshow(frame, meter)
    
#     sumValue = 0

#     #    
#     #cv2.imshow('Pose Classification', frame)    
#     pic = cv2.imread('photos/image{}.jpg'.format(x))
#     pic = cv2.resize(pic, (600,900))
#     #cv2.imshow('Sample Image',pic)
#     #Retreive the ASCII code of the key pressed
#     #k = cv2.waitKey(1) & 0xFF
    
#     # Check if 'ESC' is pressed.
#     #if(k == 27):
#       #break
#     #jpeg = cv2.imencode('.jpg', frame)
#   #return (jpeg.tobyte())
      
#   #return (jpeg.tobytes())

#   # Release the VideoCapture object and close the windows.
# camera_video.release()
# cv2.destroyAllWindows()





