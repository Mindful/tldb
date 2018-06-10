import falcon
import translation_handler
import sqlite3
import logging

# gunicorn server:app


TEXT = 'text'
SOURCE = 'source'
EXTERNAL_ID = 'external_id'


class GetContentRouting:
    def on_get(self, req, resp, source, content_id, language):
        content_id = int(content_id)
        resp.status = falcon.HTTP_200
        resp.media = {"text": "contents" + str(id)}


class GetSentenceRouting:
    def on_get(self, req, resp, source, content_id, language, sentence_number):
        content_id = int(content_id)
        sentence_number = int(sentence_number) - 1 #Sentences are 0 indexed
        source = source.lower()
        try:
            sentence = handler.get_sentence(content_id, source, sentence_number, language)
            resp.status = falcon.HTTP_200
            resp.media = vars(sentence)

        except translation_handler.ContentNotFoundException as ex:
            logger.warning("Could not find content with source %s and ID %d", source, content_id)
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
            external_id = int(content[EXTERNAL_ID])
            external_source = content[SOURCE].lower()
            handler.register_content(content[TEXT], external_id, external_source)
            resp.status = falcon.HTTP_201
        except sqlite3.IntegrityError as sqlite_ex:
            logger.exception(sqlite_ex)
            raise falcon.HTTPConflict(description="Unable to save content due to SQlite3 integrity error. Is the content a duplicate?")
        except Exception as ex:
            logger.exception(ex)
            raise falcon.HTTPInternalServerError()


app = falcon.API()
# TODO: configure logger instance, add timestamps
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
handler = translation_handler.TranslationHandler()

app.add_route('/content', NewContentRouting())
app.add_route('/content/{source}/{content_id}/{language}', GetContentRouting())
app.add_route('/content/{source}/{content_id}/{language}/{sentence_number}', GetSentenceRouting())