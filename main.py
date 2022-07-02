from typing import Union
from fastapi import FastAPI

import cv2

app = FastAPI()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/image")
def image():
  ret, frame = cap.read()
  return frame

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
  return {"item_id": item_id, "q": q}
