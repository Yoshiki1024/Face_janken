
import asyncio
import glob
import io
import os
import sys
import time
import uuid
import cv2
import time
import pygame
import time
import requests
from io import BytesIO
from urllib.parse import urlparse
 

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import (OperationStatusType,
                                                        Person,
                                                        SnapshotObjectType,
                                                        TrainingStatusType)
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageDraw, ImageFont
from mutagen.mp3 import MP3 as mp3

filename = 'battle_music.mp3' #再生したいmp3ファイル
pygame.mixer.init()
pygame.mixer.music.load(filename) #音源を読み込み
mp3_length = mp3(filename).info.length #音源の長さ取得
pygame.mixer.music.play(-1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
se = pygame.mixer.Sound('janken.wav')





capture = cv2.VideoCapture(1)
capture.set(cv2.CAP_PROP_FPS, 30)
emotion_name = ["happiness", "surprise", "fear", "anger", "sadness", "disgust", "contempt"]
user = []
rock = 'rock.png'
paper = 'paper.png'
scissors = 'scissors.png'
hebi = 'hebi.png'
kaeru = 'kaeru.png'
namekuji = 'namekuji.png'
detect = False
HP = cv2.imread("HP.png")
win = cv2.imread("win.png")
win = cv2.resize(win, (150, 50))
lose = cv2.imread("lose.png")
lose = cv2.resize(lose, (200, 50))
damage = cv2.imread("damage.png")
damage = cv2.resize(damage,(50,50))
HP = cv2.resize(HP, (50,50))
HP1 = 3
HP2 = 3

start = time.time()
print("読み込み完了")
# 認識された顔周辺に四角を描く関数
def getRectangle(faceDictionary):
       rect = faceDictionary.face_rectangle
       left = rect.left
       top = rect.top
       right = left + rect.width
       bottom = top + rect.height

    
       return ((left, top), (right, bottom))
 
# 認識された顔の上に年齢を描く関数
def get_emotion(faceDictionary):
       rect = faceDictionary.face_rectangle
       left = rect.left
       top = rect.top - 20
    
       return (left, top)
# ローカル環境変数よりキーとエンドポイントを取得
KEY1 = "f4965d368c9c45a182af90b64db65016"
ENDPOINT1 = "https://camera1.cognitiveservices.azure.com/"
KEY2 = "1a950c1098174deca1e9bec2dd663a40"
ENDPOINT2 = "https://test200.cognitiveservices.azure.com/"
 
# サブスクリプションキー情報を使用してインスタンス化
face_client1 = FaceClient(ENDPOINT1, CognitiveServicesCredentials(KEY1))
face_client2 = FaceClient(ENDPOINT2, CognitiveServicesCredentials(KEY2))

i = 1
flag = True
captures = []

while(flag):
    capture = cv2.VideoCapture(i)
    ret, frame = capture.read()
    flag = ret
    if flag:
       i += 1
       captures.append(capture)

while(True):
    emotion = []
    end = time.time()
    for i, capture in enumerate(captures):
        if i == 0 and detect == False:
            ret, frame1 = capture.read()
            cv2.imwrite('image'+ str(i+1)+'.png',frame1)
        elif i == 1 and detect == False:
            ret,frame2 = capture.read()
            cv2.imwrite('image'+ str(i+1)+'.png',frame2)
        if end - start >= 4:
    # 画像のフルパスを入力
            image_path1 = 'image1.png'
            image_path2 = 'image2.png'
    # 画像名
            image_name = os.path.basename(image_path1)
    # read binary。バイナリファイルの読み込み
            if i == 0:
                image_data1 = open(image_path1, 'rb')
                detected_faces1 = face_client1.face.detect_with_stream(image_data1,
                                    return_face_landmarks=True,
                                    return_face_attributes=['accessories','age','emotion','gender','glasses','hair','makeup','smile'])
                #detect = True
                print("b")
                if not detected_faces1:
	            #raise Exception('画像から顔を検出できませんでした。 {}'.format(image_name))
                    #detect = False
                    continue
            else:
                image_data2 = open(image_path2, 'rb')
                detected_faces2 = face_client2.face.detect_with_stream(image_data2,
                                    return_face_landmarks=True,
                                    return_face_attributes=['accessories','age','emotion','gender','glasses','hair','makeup','smile'])
                print("c")
                if not detected_faces2:
	            #raise Exception('画像から顔を検出できませんでした。 {}'.format(image_name))
                    print("c")
                    start = time.time()
                    continue
 
# イメージオブジェクト生成
            image_data1 = cv2.imread(image_path1)
            image_data2 = cv2.imread(image_path2)
 
            # 関数を呼び出して、顔に四角を描く
            #カメラ1--------------------------------------------------------------------------
            if i == 0:
                for face in detected_faces1:
                    print("カメラ1")
                    
                    num = 0
                    left1 = []
                    top1 = []
                    right1 = []
                    bottom1 = []
                    cv2.waitKey(1000)
                    (a,b),(c,d) = getRectangle(face)
                    left1.append(a)
                    top1.append(b)
                    right1.append(c)
                    bottom1.append(d)
                    print(getRectangle(face))
                    cv2.rectangle(image_data1,(left1[num],top1[num]),(right1[num],bottom1[num]), (153,132,189), 3)
                    #cv2.rectangle(image_data2,(left[num],top[num]),(right[num],bottom[num]), (153,132,189), 3)
                    print(str(face.face_attributes.emotion))
                    emotion.append(face.face_attributes.emotion.happiness)
                    emotion.append(face.face_attributes.emotion.surprise)
                    emotion.append(face.face_attributes.emotion.fear)
                    emotion.append(face.face_attributes.emotion.anger)
                    emotion.append(face.face_attributes.emotion.sadness)
                    emotion.append(face.face_attributes.emotion.disgust)
                    emotion.append(face.face_attributes.emotion.contempt)
                    max_value = max(emotion)
                    max_index = emotion.index(max_value)
                    print(emotion_name[max_index] + ":" + str(max(emotion)))
                    emotion.clear()
                    if i == 0 and top1[i] - 100 >= 0:
                        detect = True
                        if max_index == 0 :
                            hand1 = 0
                            happiness1 = max_value
                        elif max_index == 1 or max_index == 2:
                            hand1 = 1
                        else :
                            hand1 = 2
                        print("hand1:" + str(hand1))
                        num = num+1
                        #cv2.imshow("frame1", image_data1)
                        #cv2.imwrite("frame1.png", image_data1)
                        #cv2.waitKey(1)

            #カメラ2----------------------------------------------------------------------------------------
            if i == 1:
                for face in detected_faces2:
                    print("カメラ2")
                    if detect == True:
                        if HP1 == 1 :
                            image_data1[0:50,0:50] = HP #1つ目のライフ
                            image_data1[0:50,50:100] = damage #"2つ目のライフ"
                            image_data1[0:50,100:150] = damage #3つ目のライフ
                        elif HP1 == 2:
                            image_data1[0:50,0:50] = HP #1つ目のライフ
                            image_data1[0:50,50:100] = HP #"2つ目のライフ"
                            image_data1[0:50,100:150] = damage #3つ目のライフ

                        elif HP1 == 3:
                            image_data1[0:50,0:50] = HP #1つ目のライフ
                            image_data1[0:50,50:100] = HP #"2つ目のライフ"
                            image_data1[0:50,100:150] = HP #3つ目のライフ

                        if HP2 == 1:
                            image_data2[0:50,0:50] = HP #1つ目のライフ
                            image_data2[0:50,50:100] = damage #"2つ目のライフ"
                            image_data2[0:50,100:150] = damage #3つ目のライフ
                        elif HP2 == 2:
                            image_data2[0:50,0:50] = HP #1つ目のライフ
                            image_data2[0:50,50:100] = HP #"2つ目のライフ"
                            image_data2[0:50,100:150] = damage #3つ目のライフ
                        elif HP2 == 3:
                            image_data2[0:50,0:50] = HP #1つ目のライフ
                            image_data2[0:50,50:100] = HP #"2つ目のライフ"
                            image_data2[0:50,100:150] = HP #3つ目のライフ
                    cv2.imshow("frame1", image_data1)
                    cv2.imshow("frame2", image_data2)
                    cv2.waitKey(1000)
                    num = 0
                    left2 = []
                    top2 = []
                    right2 = []
                    bottom2 = []
                    (a,b),(c,d) = getRectangle(face)
                    left2.append(a)
                    top2.append(b)
                    right2.append(c)
                    bottom2.append(d)
                    print(getRectangle(face))
                    #cv2.rectangle(image_data1,(left1[num],top1[num]),(right1[num],bottom1[num]), (153,132,189), 3)
                    cv2.rectangle(image_data2,(left2[num],top2[num]),(right2[num],bottom2[num]), (153,132,189), 3)
                    print(str(face.face_attributes.emotion))
                    emotion.append(face.face_attributes.emotion.happiness)
                    emotion.append(face.face_attributes.emotion.surprise)
                    emotion.append(face.face_attributes.emotion.fear)
                    emotion.append(face.face_attributes.emotion.anger)
                    emotion.append(face.face_attributes.emotion.sadness)
                    emotion.append(face.face_attributes.emotion.disgust)
                    emotion.append(face.face_attributes.emotion.contempt)
                    max_value = max(emotion)
                    max_index = emotion.index(max_value)
                    print(emotion_name[max_index] + ":" + str(max(emotion)))
                    emotion.clear()
                    
                    if i == 1 and top2[num] - 100 >= 0 and detect:
                        image_data1 = cv2.imread("frame1.png")
                        if max_index == 0 :
                            hand2 = 0
                            img = cv2.imread(rock)
                            img = cv2.resize(img,(50,50))
                            img2 = cv2.imread(kaeru)
                            img2 = cv2.resize(img2,(50,50))
                            size = img.shape
                            size2 = img2.shape
                            image_data2[top2[num] - size[0]:top2[num],left2[num] + 50:left2[num] + 100] = img
                            image_data2[top2[num] - size2[0] - size[0]:top2[num] - size[0],left2[num] + 50:left2[num] + 100] = img2
                            happiness2 = max_value
                            if detect == True:
                                if hand1 == 2:
                                    img = cv2.imread(paper)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(namekuji)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP2 = HP2-1
                                    print("a")
                                    if HP2 == 0:
                                        image_data2[0:50,0:50] = damage #1つ目のライフ
                                        image_data2[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data2[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data1[0:50,0:150] = win
                                        image_data2[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == 1:
                                    img = cv2.imread(scissors)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(hebi)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP1 = HP1-1
                                    if HP1 == 0:
                                        image_data1[0:50,0:50] = damage #1つ目のライフ
                                        image_data1[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data1[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data2[0:50,0:150] = win
                                        image_data1[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == 0 and happiness1 > happiness2:
                                    HP2 = HP1-1
                                    img = cv2.imread(rock)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(kaeru)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    if HP2 == 0:
                                        image_data2[0:50,0:50] = damage #1つ目のライフ
                                        image_data2[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data2[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data1[0:50,0:150] = win
                                        image_data2[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == 0 and happiness1 < happiness2:
                                    HP1 = HP1-1
                                    img = cv2.imread(rock)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(kaeru)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    if HP1 == 0:
                                        image_data1[0:50,0:50] = damage #1つ目のライフ
                                        image_data1[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data1[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data2[0:50,0:150] = win
                                        image_data1[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == hand2:
                                    img = cv2.imread(rock)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(kaeru)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2

                               
                        elif max_index == 1 or max_index == 2:
                            hand2 = 1
                            img = cv2.imread(scissors)
                            img = cv2.resize(img,(50,50))
                            img2 = cv2.imread(hebi)
                            img2 = cv2.resize(img2,(50,50))
                            size = img.shape
                            size2 = img2.shape
                            image_data2[top2[num] - size[0]:top2[num],left2[num] + 50:left2[num] + 100] = img
                            image_data2[top2[num] - size2[0] - size[0]:top2[num] - size[0],left2[num] + 50:left2[num] + 100] = img2
                            if detect == True:
                                if hand1 == 2:
                                    img = cv2.imread(paper)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(namekuji)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP1 = HP1-1
                                    if HP1 == 0:
                                        image_data1[0:50,0:50] = damage #1つ目のライフ
                                        image_data1[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data1[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data2[0:50,0:150] = win
                                        image_data1[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == 0:
                                    img = cv2.imread(rock)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(kaeru)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP2 = HP2-1
                                    if HP2 == 0:
                                        image_data2[0:50,0:50] = damage #1つ目のライフ
                                        image_data2[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data2[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data1[0:50,0:150] = win
                                        image_data2[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == hand2:
                                    img = cv2.imread(scissors)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(hebi)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                               
                        else :
                            hand2 = 2
                            img = cv2.imread(paper)
                            img = cv2.resize(img,(50,50))
                            img2 = cv2.imread(namekuji)
                            img2 = cv2.resize(img2,(50,50))
                            size = img.shape
                            size2 = img2.shape
                            image_data2[top2[num] - size[0]:top2[num],left2[num] + 50:left2[num] + 100] = img
                            image_data2[top2[num] - size2[0] - size[0]:top2[num] - size[0],left2[num] + 50:left2[num] + 100] = img2
                            if detect == True:
                                if hand1 == 0:
                                    img = cv2.imread(rock)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(kaeru)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP1 = HP1-1
                                    if HP1 == 0:
                                        image_data1[0:50,0:50] = damage #1つ目のライフ
                                        image_data1[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data1[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data2[0:50,0:150] = win
                                        image_data1[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == 1:
                                    img = cv2.imread(scissors)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(hebi)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                    HP2 = HP2-1
                                    if HP2 == 0:
                                        image_data2[0:50,0:50] = damage #1つ目のライフ
                                        image_data2[0:50,50:100] = damage #"2つ目のライフ"
                                        image_data2[0:50,100:150] = damage #3つ目のライフ
                                        cv2.imshow("frame1",image_data1)
                                        cv2.imshow("frame2",image_data2)
                                        cv2.waitKey(1000)
                                        image_data1[0:50,0:150] = win
                                        image_data2[0:50,0:200] = lose
                                        HP1 = 3
                                        HP2 = 3
                                elif hand1 == hand2:
                                    img = cv2.imread(paper)
                                    img = cv2.resize(img,(50,50))
                                    img2 = cv2.imread(namekuji)
                                    img2 = cv2.resize(img2,(50,50))
                                    size = img.shape
                                    size2 = img2.shape
                                    image_data1[top1[num] - size[0]:top1[num],left1[num] + 50:left1[num] + 100] = img
                                    image_data1[top1[num] - size2[0] - size[0]:top1[num] - size[0],left1[num] + 50:left1[num] + 100] = img2
                                
                        print("hand2:" + str(hand2))
                        num = num+1
                        cv2.imshow("frame1", image_data1)
                        cv2.imshow("frame2", image_data2)
                        cv2.waitKey(3000)
                        detect = False
        else:
            if i == 0:
                cv2.imshow('frame' + str(i+1), frame1)
                cv2.waitKey(1)
                detect = False
            elif i == 1:
                cv2.imshow('frame' + str(i+1), frame2)
                cv2.waitKey(1)
                detect = False
    if cv2. waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindouws()
