# Imports the Google Cloud client library
from google.cloud import translate
import os
import logging

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './nulab-demo-8698ee1db6cc.json'


class TranslationClient:
    google_client = translate.Client()

    def __init__(self):
        self.logger = logging.getLogger()

    def translate(self, text, target_language):
        translation = self.google_client.translate(text, target_language=target_language)
        result = translation['translatedText']
        self.logger.info("%s -> %s", text, result)
        return result

