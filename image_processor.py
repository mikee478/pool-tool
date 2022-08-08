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

			'scale_factor': 100,

			'ch0_lower_bound': 0,
			'ch1_lower_bound': 0,
			'ch2_lower_bound': 0,
			'ch0_upper_bound': 255,
			'ch1_upper_bound': 255,
			'ch2_upper_bound': 255,

			'dilate_kernel_radius': 1,
			'dilate_iterations': 1,
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
					if key in self._config:
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

	def _scale(self, image):
		scale = self._config['scale_factor'] / 100
		image = cv2.resize(image, (0,0), fx=scale, fy=scale)
		return image

	def _crop(self, image):
		h,w,_ = image.shape
		image = image[
			int(h * self._config['crop_top_pct'] / 100) : int(h * (1-self._config['crop_bottom_pct'] / 100)),
			int(w * self._config['crop_left_pct'] / 100) : int(w * (1-self._config['crop_right_pct'] / 100))
		]
		return image

	def _dilate(self, image):
		s = 1 + 2 * self._config['dilate_kernel_radius']
		kernel = np.ones((s,s), np.uint8)
		im_dilate = cv2.dilate(image, kernel, iterations=self._config['dilate_iterations'])
		# im_dilate  = cv2.erode(im_dilate, kernel, iterations=self._config['dilate_iterations'])
		return im_dilate

	def _hsv_filter(self, image):
		# convert to hsv
		im_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

		# create hsv filter
		mask = cv2.inRange(im_hsv, 
			(self._config['ch0_lower_bound'], self._config['ch1_lower_bound'], self._config['ch2_lower_bound']), 
			(self._config['ch0_upper_bound'], self._config['ch1_upper_bound'], self._config['ch2_upper_bound']))
		
		# convert to rgb
		im_rgb = cv2.cvtColor(im_hsv, cv2.COLOR_HSV2RGB)

		# apply fitler
		im_filtered = cv2.bitwise_and(im_rgb, im_rgb, mask=mask)

		return im_filtered

	def _contours(self, image):
		# find contours on filtered image
		im_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		contours, hierarchy = cv2.findContours(im_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		im_contours = np.copy(image)

		if contours:
			max_area_cont = max(contours, key = cv2.contourArea)
			cv2.drawContours(im_contours, [max_area_cont], 0, (0,255,0), 2)

		return im_contours

	def __call__(self, image):

		im_scale = self._scale(image)
		im_crop = self._crop(im_scale)
		im_dilate = self._dilate(im_crop)
		im_filtered = self._hsv_filter(im_dilate)
		im_contours = self._contours(im_filtered)

		return im_crop, im_dilate, im_filtered, im_contours
