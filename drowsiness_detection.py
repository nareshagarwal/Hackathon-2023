import cv2
import dlib
import time
import playsound
import numpy as np
from threading import Thread


def play_alarm(alarm_path):
    while True:
        if kill_thread:
            break
        if blow_alarm == True:
            playsound.playsound(alarm_path)


def euclidean(A, B):
    dist1 = pow((pow(abs(A[0] - B[0]), 2) + pow(abs(A[1] - B[1]), 2)), 0.5)
    return dist1


def EAR(eye_loc):
    A = euclidean(eye_loc[1], eye_loc[5])
    B = euclidean(eye_loc[2], eye_loc[4])

    C = euclidean(eye_loc[0], eye_loc[3])

    ear = ((A + B) / (2.0 * C))

    return ear


def resize_new(image):
    (h,w) = image.shape[:2]
    r = 450 / float(w)
    r_dim = (450, int(h*r))
    image = cv2.resize(image, r_dim)

    return image


ear_threshold = 0.25
frame_threshold = 25
frame_count = 0
blow_alarm = False
kill_thread = False


face_detector = dlib.get_frontal_face_detector()
face_encoder = dlib.shape_predictor("eye_prediction_model.dat")
#PATH for alarm file
alarm_path = "MV27TES-alarm.wav"


t = Thread(target=play_alarm, args=(alarm_path,))
t.deamon = True
t.start()


v = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)


while True:
    _, frame = v.read()
    #cv2.imshow("frame",frame)

    frame = resize_new(frame)
    gray_img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_detector(gray_img)

    for face in faces:
        eye_loc = face_encoder(gray_img,face)

        coords = np.zeros((eye_loc.num_parts, 2), dtype=int)

        # encoder returns a shape type object
        # convert it to a list of tupples x,y
        for i in range(0, eye_loc.num_parts):
            coords[i] = (eye_loc.part(i).x, eye_loc.part(i).y)

        eye_loc = coords
        left_eye_loc = eye_loc[0:6]
        right_eye_loc = eye_loc[6:12]

        left_ear = EAR(left_eye_loc)
        right_ear = EAR(right_eye_loc)

        ear = ((left_ear + right_ear) / 2.0)

        for x,y in eye_loc:
            cv2.circle(frame, (x,y), 1, (0, 255, 0), -1)


        if ear < ear_threshold:
            frame_count += 1

            if frame_count >= frame_threshold:
                print("DROWSINESS DETECTED!!  BLOW ALARM!!")
                cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if not blow_alarm:
                    blow_alarm = True


        else:
            frame_count = 0
            blow_alarm = False

        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    quitKey = cv2.waitKey(1)
    if quitKey == ord('q'):
        kill_thread = True
        break

cv2.destroyAllWindows()
v.release()
cv2.destroyAllWindows()