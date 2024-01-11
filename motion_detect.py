from gpiozero import LED
from gpiozero import MotionSensor
import threading
import time

TOKENS = ["fiBV0p7yT6inq_ehASF6Hn:APA91bG4zmbp-8U16pyMdyfIMETJsU2s1fvGoXzDonTPVgKETE67_qynHT4t50QK2hUCZ6TeMHclc0c1PyI8P7DzNncb6apsUbv2iodKdpK8-itFiuazSvLsGVSHncSogEgscTc946bU"]

green_led = LED(17)
pir = MotionSensor(4)
green_led.off()

while True:
    pir.wait_for_motion()
    print("Motion Detected.")
    green_led.on()
    pushNotification(title="Guests at home.",msg="There are some ")
    pir.wait_for_no_motion()
    green_led.off()
    print("Motion stopped.")