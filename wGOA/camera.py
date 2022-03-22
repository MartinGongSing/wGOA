# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
# from imutils.video import VideoStream
# import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings


class IPWebCam(object):
	def __init__(self):
		self.url = "https://webx.ubi.pt/~goa/DATA/webcam/DCS-910.jpg"


	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		imgResp = urllib.request.urlopen(self.url)
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,-1)
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream
		# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# faces_detected = face_detection_webcam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
		# for (x, y, w, h) in faces_detected:
		# 	cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
		resize = cv2.resize(img, (640, 480), interpolation = cv2.INTER_LINEAR)
		# frame_flip = cv2.flip(resize,1)
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()
