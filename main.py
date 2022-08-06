import cv2
import numpy as np
from config import WINDOW_NAME, K_UP, K_DOWN, K_LEFT, K_RIGHT

def initialize():
	# create window
	cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

def capture_screenshot():
	# load image from a file
	screenshot = cv2.imread('screenshot.jpeg', cv2.IMREAD_COLOR)

	# crop image
	screenshot = screenshot[400:-110,150:-150]

	# scale image
	# scale = 0.8
	# screenshot = cv2.resize(screenshot, (0,0), fx=scale, fy=scale)

	return screenshot

def save_color_filter(color_filter):
	with open('color_filter.txt', 'w') as f:
		for i in range(6):
			f.write(str(color_filter[i//3][i%3])+'\n')

def load_color_filter():
	color_filter = np.zeros((2,3), dtype=int)
	with open('color_filter.txt', 'r') as f:
		for i,line in enumerate(f.readlines()):
			color_filter[i//3][i%3]= int(line)
	return color_filter

def adjust_color_filter(color_filter, channel, bound, dx):
	color_filter[bound][channel] = np.clip(color_filter[bound][channel] + dx,0,255)


screenshot = capture_screenshot()
color_filter = load_color_filter()

edit_channel = 0
	
while 1:	
	screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)

	# preparing the mask to overlay
	mask = cv2.inRange(screenshot, color_filter[0], color_filter[1])

	screenshot = cv2.cvtColor(screenshot, cv2.COLOR_HSV2RGB)

	filtered = cv2.bitwise_and(screenshot, screenshot, mask=mask)

	image = np.hstack((screenshot, filtered))

	cv2.imshow(WINDOW_NAME, image)

	key = cv2.waitKeyEx(0)
	# print(key)
	if key == 27:
		break
	elif key == ord('s'):
		save_color_filter(color_filter)
		print('Saved')
	elif key == ord('l'):
		color_filter = load_color_filter()
		print('Loaded')
	elif key == ord('1'):
		edit_channel = 0
	elif key == ord('2'):
		edit_channel = 1
	elif key == ord('3'):
		edit_channel = 2
	elif key == K_UP:
		adjust_color_filter(color_filter, edit_channel, 1, 1)
	elif key == K_DOWN:
		adjust_color_filter(color_filter, edit_channel, 1, -1)
	elif key == K_LEFT:
		adjust_color_filter(color_filter, edit_channel, 0, -1)
	elif key == K_RIGHT:
		adjust_color_filter(color_filter, edit_channel, 0, 1)

	print(color_filter, '\n')

cv2.destroyAllWindows()