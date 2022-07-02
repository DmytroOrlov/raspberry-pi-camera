from typing import Union
import io
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import cv2

app = FastAPI()

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
