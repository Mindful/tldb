import falcon
import translation_handler

#gunicorn server:app


class ArticleRouting:
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		resp.media = {"text": "Articles" + str(id)}

	def on_post(self, req, resp):
		article_text = message = req.media.get('article')
		#TODO: return something other than 200 if we fail to register the article
		handler.register_article(article_text)
		resp.status = falcon.HTTP_200



class SentenceRouting:
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		resp.media = {"text": "Sentences" + str(id)}

# falcon.API instances are callable WSGI apps
app = falcon.API()
handler = translation_handler.TranslationHandler()

# Resources are represented by long-lived class instances that handle all the requests at a url
app.add_route('/article/{id}', ArticleRouting())
app.add_route('/sentence/{id}', SentenceRouting())