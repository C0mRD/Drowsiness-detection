import cv2
import numpy as np
import dlib
from imutils import face_utils
import gtts
from playsound import playsound

def distace(ptA,ptB):
    dis = np.linalg.norm(ptA-ptB)
    return dis
def blinked(a,b,c,d,e,f):
    vertical = distace(b,d) + distace(c,e)
    horizontal = distace(a,f)
    ear = vertical/(2.0*horizontal)
    uLimit = 0.24
    lLimit = 0.18
    if(ear > uLimit):
        return 2
    elif(ear > lLimit and ear <=uLimit):
        return 1
    else:
        return 0

def sound(text):
    tts = gtts.gTTS(text)
    tts.save('sound.mp3')
    playsound('sound.mp3')

def main():
    cap = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    sleep = 0
    drowsy = 0
    active = 0
    status = ''
    color = (0, 0, 0)
    maxtime = 6

    while cap.isOpened():
        _,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

            landmarks = predictor(gray,face)
            landmarks = face_utils.shape_to_np(landmarks) #Q

            leftBlink = blinked(landmarks[36],landmarks[37],landmarks[38],
                                landmarks[41],landmarks[40],landmarks[39])
            rightBlink = blinked(landmarks[42],landmarks[43],landmarks[44],
                                 landmarks[47],landmarks[46],landmarks[45])

            if(leftBlink==0 and rightBlink==0):
                sleep+=1
                drowsy=0
                active=0
                if(sleep>maxtime):
                    status='SLEEPING !!!'
                    color=(0,0,255)
                    sound('Warning sleeping')

            elif (leftBlink == 1 and rightBlink == 1):
                sleep = 0
                drowsy+= 1
                active = 0
                if (drowsy > maxtime):
                    status = 'Drowsy...'
                    color = (255, 0, 0)
                    sound('Drowsy')

            else:
                sleep = 0
                drowsy = 0
                active += 1
                if (active > maxtime):
                    status = 'ACTIVE'
                    color = (0, 255, 0)

            cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            for n in range(0,68):
                (x,y) = landmarks[n]
                cv2.circle(frame,(x,y),1,(255,255,255),-1)

        cv2.imshow("Result of Detector",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    main()
