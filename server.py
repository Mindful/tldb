import falcon
import translation_handler
import sqlite3
from datetime import datetime
import logging

#gunicorn server:app


TEXT = 'text'
SOURCE = 'source'
EXTERNAL_ID = 'external_id'

class GetContentRouting:
	def on_get(self, req, resp, source, id, language):
		resp.status = falcon.HTTP_200
		resp.media = {"text": "contents" + str(id)}


class GetSentenceRouting:
	def on_get(self, req, resp, source, id, language, sentence_number):
		try:
			sentence = handler.get_sentence(source, id, sentence_number, language)
			resp.status = falcon.HTTP_200
			resp.media = {vars(sentence)}

		except translation_handler.ContentNotFoundException as ex:
			logger.warning(ex)
			raise falcon.HTTPNotFound(description="Could not find content with the specified source and ID")
		except Exception as ex:
			logger.exception(ex)
			raise falcon.HTTPInternalServerError()


class NewContentRouting:
	def on_post(self, req, resp):
		content = req.media.get('content')
		for required_attribute in [TEXT, SOURCE, EXTERNAL_ID]:
			if required_attribute not in content:
				raise falcon.HTTPBadRequest(description="Missing required attribute: " + required_attribute)

		try:
			handler.register_content(content[TEXT], content[EXTERNAL_ID], content[SOURCE])
			resp.status = falcon.HTTP_201
		except sqlite3.IntegrityError as sqlite_ex:
			logger.exception(sqlite_ex)
			raise falcon.HTTPConflict(description="Unable to save content due to SQlite3 integrity error. Is the content a duplicate?")
		except Exception as ex:
			logger.exception(ex)
			raise falcon.HTTPInternalServerError()






app = falcon.API()
#TODO: configure logger instance, add timestamps
logger = logging.getLogger()
handler = translation_handler.TranslationHandler(logger)

app.add_route('/content', NewContentRouting())
app.add_route('/content/{source}/{id}/{language}', GetContentRouting())
app.add_route('/content/{source}/{id}/{language}/{sentence_number}', GetSentenceRouting())