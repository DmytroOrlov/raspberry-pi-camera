from typing import Union
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import cv2

from PCA9685 import PCA9685


class Servo:
  def __init__(self):
    self.PwmServo = PCA9685(0x40, debug=True)
    self.PwmServo.setPWMFreq(50)
    self.PwmServo.setServoPulse(8, 1500)
    self.PwmServo.setServoPulse(9, 1500)

  def setServoPwm(self, channel, angle, error=12):
    angle = int(angle)
    if channel == '0':
      error = 18
      self.PwmServo.setServoPulse(8, 2500 - int((angle + error) / 0.09))
    elif channel == '1':
      self.PwmServo.setServoPulse(9, 500 + int((angle + error) / 0.09))
    elif channel == '2':
      self.PwmServo.setServoPulse(10, 500 + int((angle + error) / 0.09))
    elif channel == '3':
      self.PwmServo.setServoPulse(11, 500 + int((angle + error) / 0.09))
    elif channel == '4':
      self.PwmServo.setServoPulse(12, 500 + int((angle + error) / 0.09))
    elif channel == '5':
      self.PwmServo.setServoPulse(13, 500 + int((angle + error) / 0.09))
    elif channel == '6':
      self.PwmServo.setServoPulse(14, 500 + int((angle + error) / 0.09))
    elif channel == '7':
      self.PwmServo.setServoPulse(15, 500 + int((angle + error) / 0.09))

app = FastAPI()
pwm=Servo()
pwm.setServoPwm('0', 90)
pwm.setServoPwm('1', 90)

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
