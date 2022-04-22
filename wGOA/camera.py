# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
# from imutils.video import VideoStream
# import imutils
import os,urllib.request
import numpy as np
from django.conf import settings
import cv2


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

		resize = cv2.resize(img, (640, 480), interpolation = cv2.INTER_LINEAR)
		# frame_flip = cv2.flip(resize,1) #if we want to flip the image
		ret, jpeg = cv2.imencode('.jpg', resize)
		return jpeg.tobytes()
