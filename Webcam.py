import cv
from cv import CV_CAP_PROP_FRAME_WIDTH as FRAME_WIDTH
from cv import CV_CAP_PROP_FRAME_HEIGHT as FRAME_HEIGHT
import numpy as N

from Camera import *

def ipl2array(im):
	'''Converts an IplImage @im to a NumPy array.
	Adapted from http://opencv.willowgarage.com/wiki/PythonInterface'''
	depth2dtype = {
		cv.IPL_DEPTH_8U: 'uint8',
		cv.IPL_DEPTH_8S: 'int8',
		cv.IPL_DEPTH_16U: 'uint16',
		cv.IPL_DEPTH_16S: 'int16',
		cv.IPL_DEPTH_32S: 'int32',
		cv.IPL_DEPTH_32F: 'float32',
		cv.IPL_DEPTH_64F: 'float64',
	}
	
	a = N.fromstring(im.tostring(),
		             dtype=depth2dtype[im.depth],
		             count=im.width * im.height * im.nChannels)
	a.shape = (im.height, im.width, im.nChannels)
	return a 

class Webcam(Camera):
	def __init__(self, *args, **kwargs):
		Camera.__init__(self, *args, **kwargs)
		self._capture = None
	
	def open(self):
		self._capture = cv.CaptureFromCAM(self.camera_number)
		
		# doesn't raise an exception on error, so we test it explicitly
		iplimage = cv.QueryFrame(self._capture)
		if iplimage is None:
			raise CameraError('Could not query image', self.camera_number)
	
	def close(self):
		cv.ReleaseCapture(self._capture)
	
	def query_frame(self):
		iplimage = cv.QueryFrame(self._capture)
		if iplimage is None:
			raise CameraError('Could not query image', self.camera_number)
		self.frame = ipl2array(iplimage)

	@property
	def resolution(self):
		'''Resolution of the webcam - a 2-tuple'''
		width = cv.GetCaptureProperty(self._capture, FRAME_WIDTH)
		height = cv.GetCaptureProperty(self._capture, FRAME_HEIGHT)
		return (int(width), int(height))
	
	@resolution.setter
	def resolution(self, value):
		width, height = value
		cv.SetCaptureProperty(self._capture, FRAME_WIDTH, width)
		cv.SetCaptureProperty(self._capture, FRAME_HEIGHT, height)
		if cv.GetCaptureProperty(self._capture, FRAME_WIDTH) != width:
			raise CameraError('Width {0} not supported'.format(width), self.camera_number)
		if cv.GetCaptureProperty(self._capture, FRAME_HEIGHT) != height:
			raise CameraError('Height {0} not supported'.format(height), self.camera_number)
