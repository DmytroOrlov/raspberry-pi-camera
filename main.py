import time
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import cv2

app = FastAPI()

from servo import *

pwm = Servo()
pwm.setServoPwm('0', 90)
pwm.setServoPwm('1', 90)

from Led import *

led = Led()
led.colorWipe(led.strip, Color(0, 0, 0))

from Motor import *

PWM = Motor()
PWM.setMotorModel(0, 0, 0, 0)

from Ultrasonic import *

ultrasonic = Ultrasonic()


@app.get("/")
def image():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
    # for ii in range(10):
    #   cap.grab()
    res, frame = cap.read()
    res, im_jpeg = cv2.imencode(".jpeg", frame)
    cap.release()
    return StreamingResponse(io.BytesIO(im_jpeg.tobytes()), media_type="image/jpeg")


@app.get("/led")
def led_on(r: int, g: int, b: int):
    led.ledIndex(0x01, r, g, b)
    led.ledIndex(0x02, r, g, b)
    led.ledIndex(0x04, r, g, b)
    led.ledIndex(0x08, r, g, b)
    led.ledIndex(0x10, r, g, b)
    led.ledIndex(0x20, r, g, b)
    led.ledIndex(0x40, r, g, b)
    led.ledIndex(0x80, r, g, b)
    return ""


@app.get("/led-off")
def led_off():
    led.colorWipe(led.strip, Color(0, 0, 0))
    return ""


@app.get("/run")
def run():
    for i in range(85, 96, 10):
        pwm.setServoPwm('0', i)
        pwm.setServoPwm('1', 75)
        time.sleep(0.2)
        if i == 85:
            L = ultrasonic.get_distance()
        else:
            R = ultrasonic.get_distance()
    if L > 40 and R > 40:
        PWM.setMotorModel(650, 650, 650, 650)
        time.sleep(0.4)
    else:
        PWM.setMotorModel(-550, -550, -550, -550)
        time.sleep(0.3)
    PWM.setMotorModel(0, 0, 0, 0)
    return ""
