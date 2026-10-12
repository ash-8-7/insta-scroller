"""
camera.py
---------
Thin wrapper around OpenCV's VideoCapture.
Only opens, reads, and releases the webcam.
No gesture logic belongs here.
"""

import cv2


class Camera:
    def __init__(self, index=0, width=640, height=480, mirror=True):
        self.index = index
        self.width = width
        self.height = height
        self.mirror = mirror
        self.cap = None

    def open(self):
        """Open the camera. Raises RuntimeError if it can't be opened."""
        # CAP_DSHOW is faster and more reliable on Windows.
        self.cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            # Fallback without DSHOW (non-Windows or if DSHOW fails)
            self.cap = cv2.VideoCapture(self.index)
            if not self.cap.isOpened():
                raise RuntimeError(
                    f"Could not open camera at index {self.index}. "
                    "Is another app using it? Try CAMERA_INDEX = 1."
                )
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        """Return (ok, frame). frame is BGR and mirrored if enabled."""
        if self.cap is None:
            return False, None
        ok, frame = self.cap.read()
        if not ok:
            return False, None
        if self.mirror:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None