from itertools import cycle
import pickle
import cv2
import numpy as np

class ImageProcessor:
	def __init__(self):
		self._config = {
			'crop_top_pct': 0,
			'crop_bottom_pct': 0,
			'crop_left_pct': 0,
			'crop_right_pct': 0,

			'scale_factor': 75,

			'ch0_lower_bound': 0,
			'ch1_lower_bound': 0,
			'ch2_lower_bound': 0,
			'ch0_upper_bound': 255,
			'ch1_upper_bound': 255,
			'ch2_upper_bound': 255,

			'dilation_kernel_radius': 1,
			'dilation_iterations': 1,
		}

		self.load_config()

		self._config_iter = cycle(self._config)
		self._config_key = next(self._config_iter)

	def save_config(self):
		with open('config.pickle', 'wb') as file:
			pickle.dump(self._config, file)
			print('Config Saved')

	def load_config(self):
		try:
			with open('config.pickle', 'rb') as file:
				t = pickle.load(file)
				for key,val in t.items():
					self._config[key] = val
				print('Config Loaded')
		except FileNotFoundError as e:
			print(f'Load Config Failed: {e}')

	def next_config_key(self):
		self._config_key = next(self._config_iter)
		print(f'\n{self._config_key} = {self._config[self._config_key]}')

	def adjust_config(self, val):
		self._config[self._config_key] += val
		print(f'{self._config_key} = {self._config[self._config_key]}')

	def preprocess(self, image):
		# load image from a file
		# screenshot = cv2.imread('screenshot.jpeg', cv2.IMREAD_COLOR)

		# scale image
		scale = self._config['scale_factor'] / 100
		image = cv2.resize(image, (0,0), fx=scale, fy=scale)

		# crop image
		h,w,_ = image.shape
		image = image[
			int(h * self._config['crop_top_pct'] / 100) : int(h * (1-self._config['crop_bottom_pct'] / 100)),
			int(w * self._config['crop_left_pct'] / 100) : int(w * (1-self._config['crop_right_pct'] / 100))
		]

		return image

	def __call__(self, image):
		image = self.preprocess(image)

		# dilate
		s = 1 + 2 * self._config['dilation_kernel_radius']
		kernel = np.ones((s,s), np.uint8)
		im_dilate = cv2.dilate(image, kernel, iterations=self._config['dilation_iterations'])

		# convert to hsv
		im_hsv = cv2.cvtColor(im_dilate, cv2.COLOR_RGB2HSV)

		# create hsv filter
		mask = cv2.inRange(im_hsv, 
			(self._config['ch0_lower_bound'], self._config['ch1_lower_bound'], self._config['ch2_lower_bound']), 
			(self._config['ch0_upper_bound'], self._config['ch1_upper_bound'], self._config['ch2_upper_bound']))
		
		# convert to rgb
		im_rgb = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2RGB)

		# apply fitler
		im_filtered = cv2.bitwise_and(im_rgb, im_rgb, mask=mask)

		# find contours on filtered image
		im_filtered_gray = cv2.cvtColor(im_filtered, cv2.COLOR_BGR2GRAY)
		contours, hierarchy = cv2.findContours(im_filtered_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		im_contours = np.copy(im_filtered)

		if contours:
			max_area_cont = max(contours, key = cv2.contourArea)
			cv2.drawContours(im_contours, [max_area_cont], 0, (0,255,0), 2)

		return image, im_dilate, im_filtered, im_contours
