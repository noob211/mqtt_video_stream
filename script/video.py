import cv2
import numpy as np
from threading import Thread
import time


class WebcamVideoStream(object):
    def __init__(self, name="WebcamVideoStream"):
        self.find_camera_index()
        self.video_source: int = 0
        self.stream = cv2.VideoCapture(self.video_source)
        (self.grabbed, self.frame) = self.stream.read()
        self.frame: np = np.ones((480, 640, 3), dtype=np.uint8)
        self.name: str = name
        self.stopped: bool = False
        self.color: tuple = (0, 256, 256)

    def start(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self) -> None:
        while True:
            if self.stopped:
                return
            if not self.grabbed:
                self.frame = np.ones((480, 640, 3), dtype=np.uint8)
                cv2.putText(self.frame, " FAILED TO ACCESS CAMERA ", (65, 220), cv2.FONT_HERSHEY_PLAIN, 2, self.color)
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self) -> None:
        self.stopped = True

    def find_camera_index(self) -> None:
        for i in range(0, 5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f" camera is available at {i}!")
                self.video_source = i
                cap.release()
                time.sleep(2)
                break

a = WebcamVideoStream()
a.start()
while True:
    cv2.imshow('xxxx', a.read())
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
