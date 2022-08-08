import cv2
import numpy as np

from defines import *
from screenshotter import Screenshotter
from image_processor import ImageProcessor

# create window
cv2.namedWindow(WINDOW_NAME)

screenshotter = Screenshotter(QTP_WINDOW_NAME)
image_processor = ImageProcessor()

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

cv2.destroyAllWindows()
