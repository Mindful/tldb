import configparser
import os.path


class ConfigReader:

	CONF_FILE_NAME = "config.ini"

	def __init__(self):
		self.auth = None
		if os.path.isfile(self.CONF_FILE_NAME):
			parser = configparser.ConfigParser()
			parser.read(self.CONF_FILE_NAME)

			if 'auth' in parser:
				self.auth = (parser['auth']['username'], parser['auth']['password'])
			



