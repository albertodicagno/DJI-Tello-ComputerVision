import cv2
import sys
from djitellopy import Tello

cascPath = sys.argv[1]  # percorso modello da rilevare
faceCascade = cv2.CascadeClassifier(cascPath)
drone = Tello()  # dichiaro l'oggetto drone
drone.connect()
drone.streamon()  # attivo lo streaming

# video_capture = cv2.VideoCapture("udp://0.0.0.0:11111")  #per video crudo
# video_capture = cv2.VideoCapture("rtsp://192.168.1.1")  #per video da action cam
video_capture = cv2.VideoCapture(0)  # per video da webcam

while True:
    # lettura frame per frame
    ret, frame = video_capture.read()
    # frame = drone.get_frame_read().frame  # cattura frame dal drone
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # immagine in scala di grigi

    faces = faceCascade.detectMultiScale(  # face detection
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Decorazione immagini per segnalare le facce
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)  # rettangolo di contorno
        cv2.circle(frame, (int(x+w/2), int(y+h/2)), 12, (0, 0, 255), 1)  # cerchio di mira
        print(frame.shape)

    cv2.imshow('Video', frame)  # mostra il frame sul display del pc

    if cv2.waitKey(1) & 0xFF == ord('q'):  # quit
        break

# rilascio risorse
# video_capture.release()
cv2.destroyAllWindows()
