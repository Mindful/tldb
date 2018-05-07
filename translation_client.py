# Imports the Google Cloud client library
from google.cloud import translate
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './nulab-demo-8698ee1db6cc.json'

class TranslationClient:
	google_client = translate.Client()

	def translate(self, text, target_language):
		translation = self.google_client.translate(text, target_language=target_language)
		return translation['translatedText']

