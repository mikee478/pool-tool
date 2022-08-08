import cv2
import numpy as np
from defines import WINDOW_NAME, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_S, K_L, K_ENTER, config, save_config, load_config
from screenshotter import Screenshotter
from itertools import cycle

def preprocess(screenshot):
	# load image from a file
	# screenshot = cv2.imread('screenshot.jpeg', cv2.IMREAD_COLOR)

	# crop image
	screenshot = screenshot[
	config['crop_top']:config['crop_bottom'],
	config['crop_left']:config['crop_right']]

	# scale image
	# scale = 0.75
	# screenshot = cv2.resize(screenshot, (0,0), fx=scale, fy=scale)

	return screenshot

# create window
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

load_config()

ss_file_name = 'screenshot.png'
screenshotter = Screenshotter('Movie Recording')

config_iter = cycle(config)
config_key = next(config_iter)

while 1:	

	if screenshotter.capture(ss_file_name) != 0:
		break

	# read screenshot file
	screenshot = cv2.imread(ss_file_name, cv2.IMREAD_COLOR)

	screenshot = preprocess(screenshot)

	# convert to hsv
	screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)

	# create hsv filter
	mask = cv2.inRange(screenshot, 
		(config['ch0_lower_bound'], config['ch1_lower_bound'], config['ch2_lower_bound']), 
		(config['ch0_upper_bound'], config['ch1_upper_bound'], config['ch2_upper_bound']))
	
	# convert to rgb
	screenshot = cv2.cvtColor(screenshot, cv2.COLOR_HSV2RGB)

	# apply fitler
	filtered = cv2.bitwise_and(screenshot, screenshot, mask=mask)

	# find contours on filtered image
	filtered_gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
	contours, hierarchy = cv2.findContours(filtered_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	cont_img = np.copy(filtered)

	if contours:
		max_area_cont = max(contours, key = cv2.contourArea)
		cv2.drawContours(cont_img, [max_area_cont], 0, (0,255,0), 2)

		# for x,y in np.squeeze(max_area_cont):
		# 	cont_img = cv2.circle(cont_img, (x,y), radius=2, color=(255, 0, 0), thickness=-1)

		# contours.sort(key=cv2.contourArea,reverse=True)
		# cv2.drawContours(cont_img, contours, 0, (255,0,0), 2)
		# cv2.drawContours(cont_img, contours, 1, (0,255,0), 2)
		# cv2.drawContours(cont_img, contours, 2, (0,0,255), 2)

	# concat images
	image = np.hstack((screenshot, cont_img))
	cv2.imshow(WINDOW_NAME, image)

	key = cv2.waitKeyEx(100)

	if key == K_ESCAPE:
		break
	elif key == K_S:
		save_config()
		print('Saved Config')
	elif key == K_L:
		load_config()
		print('Loaded Config', config)
	elif key == K_ENTER:
		config_key = next(config_iter)
		print(config_key)
	elif key == K_UP:
		config[config_key] += 1
		print(f'{config_key} = {config[config_key]}')
	elif key == K_DOWN:
		config[config_key] -= 1
		print(f'{config_key} = {config[config_key]}')

cv2.destroyAllWindows()
