from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2
import push_notification as pn
from gpiozero import LED
from gpiozero import MotionSensor
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180

rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

REDMI_TOKEN = "cvasUnPEQrCacGXetTRLp4:APA91bFWaly7TjM9s1t2kIFyLbtF2LBkd8JKtAZ4EjxhbE4NAPPtiZkRKBUnAyOKmxd8Zs0w1MQHn5XOMNC7JXuifcCjxI5k5d2mGv-jpCA5o-Y6Haz17lowmSoMWLXvAaZJHTNwBtx9" 
OTHER_TOKEN = "fiBV0p7yT6inq_ehASF6Hn:APA91bG4zmbp-8U16pyMdyfIMETJsU2s1fvGoXzDonTPVgKETE67_qynHT4t50QK2hUCZ6TeMHclc0c1PyI8P7DzNncb6apsUbv2iodKdpK8-itFiuazSvLsGVSHncSogEgscTc946bU"
TOKENS = [
    OTHER_TOKEN,
    REDMI_TOKEN
    ]

green_led = LED(17)
green_led.on()

pir = MotionSensor(4)

check = True
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    boxes, weights = hog.detectMultiScale(image, winStride=(8,8) )
    
    if (len(weights)>0 and pir.motion_detected):
        if (check != True):
            check = True
        green_led.off()
        pn.pushNotification(title="Guests in house.",msg=f"There are {len(weights)} guests.",registration_token = TOKENS)
    else:
        if (check == True):
         print("no human.")
         check = False
        green_led.on()
     #   green_led.off()
    
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(image, (xA, yA), (xB, yB),(0, 255, 0), 2)
    cv2.imshow("Frame", image);
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
       break
