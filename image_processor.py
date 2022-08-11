from itertools import cycle
import pickle
import cv2
import numpy as np

from defines import CONFIG_FILE

class ImageProcessor:
	def __init__(self):
		self._config = {
			'crop_top_pct': 0,
			'crop_bottom_pct': 0,
			'crop_left_pct': 0,
			'crop_right_pct': 0,

			'scale_factor': 100,

			'white_h_min': 0,
			'white_h_max': 255,
			'white_s_min': 0,
			'white_s_max': 255,
			'white_v_min': 0,
			'white_v_max': 255,

			'yellow_h_min': 0,
			'yellow_h_max': 255,
			'yellow_s_min': 0,
			'yellow_s_max': 255,
			'yellow_v_min': 0,
			'yellow_v_max': 255,

			'green_h_min': 0,
			'green_h_max': 255,
			'green_s_min': 0,
			'green_s_max': 255,
			'green_v_min': 0,
			'green_v_max': 255,

			'purple_h_min': 0,
			'purple_h_max': 255,
			'purple_s_min': 0,
			'purple_s_max': 255,
			'purple_v_min': 0,
			'purple_v_max': 255,

			'blue_h_min': 0,
			'blue_h_max': 255,
			'blue_s_min': 0,
			'blue_s_max': 255,
			'blue_v_min': 0,
			'blue_v_max': 255,

			'red_h_min': 0,
			'red_h_max': 255,
			'red_s_min': 0,
			'red_s_max': 255,
			'red_v_min': 0,
			'red_v_max': 255,

			'orange_h_min': 0,
			'orange_h_max': 255,
			'orange_s_min': 0,
			'orange_s_max': 255,
			'orange_v_min': 0,
			'orange_v_max': 255,

			'burgundy_h_min': 0,
			'burgundy_h_max': 255,
			'burgundy_s_min': 0,
			'burgundy_s_max': 255,
			'burgundy_v_min': 0,
			'burgundy_v_max': 255,

			'cue_h_min': 0,
			'cue_h_max': 255,
			'cue_s_min': 0,
			'cue_s_max': 255,
			'cue_v_min': 0,
			'cue_v_max': 255,

			'border_top_pct': 0,
			'border_bottom_pct': 0,
			'border_left_pct': 0,
			'border_right_pct': 0,

			'dilate_kernel_radius': 1,
			'dilate_iterations': 1,
		}

		self.load_config()

		self._config_iter = cycle(self._config)
		self._config_key = next(self._config_iter)

	def save_config(self):
		with open(CONFIG_FILE, 'wb') as file:
			pickle.dump(self._config, file)
			print('Config Saved')

	def load_config(self):
		try:
			with open(CONFIG_FILE, 'rb') as file:
				t = pickle.load(file)
				for key,val in t.items():
					if key in self._config:
						self._config[key] = val
				print('Config Loaded')
				print(self._config)
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

	def _hsv_filter(self, image):
		# convert to hsv
		im_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

		# create hsv masks
		white_mask = cv2.inRange(im_hsv, 
			(self._config['white_h_min'], self._config['white_s_min'], self._config['white_v_min']), 
			(self._config['white_h_max'], self._config['white_s_max'], self._config['white_v_max']))

		yellow_mask = cv2.inRange(im_hsv, 
			(self._config['yellow_h_min'], self._config['yellow_s_min'], self._config['yellow_v_min']), 
			(self._config['yellow_h_max'], self._config['yellow_s_max'], self._config['yellow_v_max']))

		green_mask = cv2.inRange(im_hsv, 
			(self._config['green_h_min'], self._config['green_s_min'], self._config['green_v_min']), 
			(self._config['green_h_max'], self._config['green_s_max'], self._config['green_v_max']))

		purple_mask = cv2.inRange(im_hsv, 
			(self._config['purple_h_min'], self._config['purple_s_min'], self._config['purple_v_min']), 
			(self._config['purple_h_max'], self._config['purple_s_max'], self._config['purple_v_max']))
		
		blue_mask = cv2.inRange(im_hsv, 
			(self._config['blue_h_min'], self._config['blue_s_min'], self._config['blue_v_min']), 
			(self._config['blue_h_max'], self._config['blue_s_max'], self._config['blue_v_max']))

		red_mask = cv2.inRange(im_hsv, 
			(self._config['red_h_min'], self._config['red_s_min'], self._config['red_v_min']), 
			(self._config['red_h_max'], self._config['red_s_max'], self._config['red_v_max']))

		orange_mask = cv2.inRange(im_hsv, 
			(self._config['orange_h_min'], self._config['orange_s_min'], self._config['orange_v_min']), 
			(self._config['orange_h_max'], self._config['orange_s_max'], self._config['orange_v_max']))

		burgundy_mask = cv2.inRange(im_hsv, 
			(self._config['burgundy_h_min'], self._config['burgundy_s_min'], self._config['burgundy_v_min']), 
			(self._config['burgundy_h_max'], self._config['burgundy_s_max'], self._config['burgundy_v_max']))

		cue_mask = cv2.inRange(im_hsv, 
			(self._config['cue_h_min'], self._config['cue_s_min'], self._config['cue_v_min']), 
			(self._config['cue_h_max'], self._config['cue_s_max'], self._config['cue_v_max']))

		mask = (white_mask | yellow_mask | green_mask | purple_mask | 
			blue_mask | red_mask | orange_mask | burgundy_mask)

		mask &= np.invert(cue_mask)
		
		border_mask = np.zeros_like(mask)
		h,w = mask.shape
		border_mask[
			int(h * self._config['border_top_pct'] / 100) : int(h * (1-self._config['border_bottom_pct'] / 100)),
			int(w * self._config['border_left_pct'] / 100) : int(w * (1-self._config['border_right_pct'] / 100))
		].fill(1)

		mask &= border_mask

		# apply masks
		im_filtered = cv2.bitwise_and(image, image, mask=mask)

		return im_filtered

	def _dilate(self, image):
		s = 1 + 2 * self._config['dilate_kernel_radius']
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(s,s))
		im_dilate = cv2.dilate(image, kernel, iterations=self._config['dilate_iterations'])
		return im_dilate

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
		im_filtered = self._hsv_filter(im_crop)
		im_dilate = self._dilate(im_filtered)
		im_contours = self._contours(im_dilate)

		return im_crop, im_filtered, im_dilate, im_contours
