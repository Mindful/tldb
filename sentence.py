class Sentence:
	def __init__(self, sentence_number, translated_text, language, article_id):
		self.article_id = article_id
		self.sentence_number = sentence_number
		self.translated_text = translated_text
		self.language = language

		