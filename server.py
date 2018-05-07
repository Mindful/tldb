import falcon

#gunicorn server:app


class ArticleRouting:
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		resp.media = {"text": "Articles" + str(id)}

	def on_post(self, req, resp):
		

class SentenceRouting:
	def on_get(self, req, resp, id):
		resp.status = falcon.HTTP_200
		resp.media = {"text": "Sentences" + str(id)}

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances that handle all the requests at a url
app.add_route('/article/{id}', ArticleRouting())
app.add_route('/sentence/{id}', SentenceRouting())