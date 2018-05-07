import translation_client
import translation_database
import spacy
import sentence


def TranslationHandler:

	languages = ['ja']

	def __init__(self):
		self.db = translation_database.TranslationDatabase()
		self.web_client = translation_client.TranslationClient()


	def register_article(self, article_text):
		article = self.db.insert_article(article)
		for language in languages:
			save_article_translations(article, language)




	def save_article_translations(self, article, language):
		output_sents = []
		for counter, sentence in enumerate(article.get_parsed_text().sents):
			sentence_number = counter + 1 # Counter starts from 0
			sentence_translation = self.web_client.translate(sentence.text)



