import cv2
import numpy as np

from defines import *
from screenshotter import Screenshotter
from image_processor import ImageProcessor

# create window
cv2.namedWindow(WINDOW_NAME)

screenshotter = Screenshotter(QTP_WINDOW_NAME)
image_processor = ImageProcessor()

##### CONFIG TUNING #####
'''
color = 'green'

def on_change(val):
	h_min = cv2.getTrackbarPos('H min', WINDOW_NAME)
	h_max = cv2.getTrackbarPos('H max', WINDOW_NAME)
	s_min = cv2.getTrackbarPos('S min', WINDOW_NAME)
	s_max = cv2.getTrackbarPos('S max', WINDOW_NAME)
	v_min = cv2.getTrackbarPos('V min', WINDOW_NAME)
	v_max = cv2.getTrackbarPos('V max', WINDOW_NAME)

	image_processor._config[f'{color}_h_min'] = h_min
	image_processor._config[f'{color}_h_max'] = h_max
	image_processor._config[f'{color}_s_min'] = s_min
	image_processor._config[f'{color}_s_max'] = s_max
	image_processor._config[f'{color}_v_min'] = v_min
	image_processor._config[f'{color}_v_max'] = v_max

cv2.createTrackbar('H min', WINDOW_NAME, image_processor._config[f'{color}_h_min'], 255, on_change)
cv2.createTrackbar('H max', WINDOW_NAME, image_processor._config[f'{color}_h_max'], 255, on_change)
cv2.createTrackbar('S min', WINDOW_NAME, image_processor._config[f'{color}_s_min'], 255, on_change)
cv2.createTrackbar('S max', WINDOW_NAME, image_processor._config[f'{color}_s_max'], 255, on_change)
cv2.createTrackbar('V min', WINDOW_NAME, image_processor._config[f'{color}_v_min'], 255, on_change)
cv2.createTrackbar('V max', WINDOW_NAME, image_processor._config[f'{color}_v_max'], 255, on_change)
'''
##### CONFIG TUNING #####

while True:	

	if screenshotter.capture(SCREENSHOT_FILE_NAME):

		# read screenshot file
		screenshot = cv2.imread(SCREENSHOT_FILE_NAME, cv2.IMREAD_COLOR)

		processed_images = image_processor(screenshot)

		# show concatted images
		im_concat = np.hstack(processed_images)
		cv2.imshow(WINDOW_NAME, im_concat)

	key = cv2.waitKeyEx(WAIT_KEY_DELAY_MS)
	if key == K_ESCAPE:
		break
	elif key == K_S:
		image_processor.save_config()
	elif key == K_L:
		image_processor.load_config()
	elif key == K_ENTER:
		image_processor.next_config_key()
	elif key == K_UP:
		image_processor.adjust_config(1)
	elif key == K_DOWN:
		image_processor.adjust_config(-1)
	elif key == K_LEFT:
		image_processor.adjust_config(-5)
	elif key == K_RIGHT:
		image_processor.adjust_config(5)

cv2.destroyAllWindows()
