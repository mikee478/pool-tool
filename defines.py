import pickle

WINDOW_NAME = 'Pool Tool'
K_ENTER = 13
K_ESCAPE = 27
K_L = 108
K_S = 115
K_UP = 63232
K_DOWN = 63233
K_LEFT = 63234
K_RIGHT = 63235

config = {
	'crop_top': 0,
	'crop_bottom': 0,
	'crop_left': 0,
	'crop_right': 0,

	'ch0_lower_bound': 0,
	'ch1_lower_bound': 0,
	'ch2_lower_bound': 0,
	'ch0_upper_bound': 255,
	'ch1_upper_bound': 255,
	'ch2_upper_bound': 255,
}

def save_config():
	with open('config.pickle', 'wb') as file:
		pickle.dump(config, file)

def load_config():
	with open('config.pickle', 'rb') as file:
		t = pickle.load(file)

		for key,val in t.items():
			config[key] = val
