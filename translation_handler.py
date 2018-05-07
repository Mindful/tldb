import translation_client
import translation_database
import spacy
import sentence


class TranslationHandler:

	languages = ['ja']

	def __init__(self):
		self.db = translation_database.TranslationDatabase()
		self.web_client = translation_client.TranslationClient()


	def register_article(self, article_text):
		article = self.db.insert_article(article)
		for language in languages:
			self.__save_article_translations(article, language)


	def __save_article_translations(self, article, language):
		output_sentence_tuples = []
		for counter, sentence in enumerate(article.get_parsed_text().sents):
			sentence_number = counter + 1 # Counter starts from 0
			sentence_translation = self.web_client.translate(sentence.text)
			output_sentence_tuples.append((sentence_number, sentence_translation, language, article.db_id))

		return self.db.create_sentences(output_sentence_tuples)




