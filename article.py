import spacy

class Article:

	#Only using sentencizing right now, so for speed we can disable the other parts of spacy
	nlp = spacy.load('en', disable=['tagger', 'parser', 'ner', 'textcat'])
	nlp.add_pipe(nlp.create_pipe("sentencizer"))

	def __init__(self, db_id, base_text):
		self.db_id = db_id
		self.base_text = base_text
		self.__parsed_text = None


	def get_parsed_text(self):
		if not self.__parsed_text:
			self.__parsed_text = self.nlp(self.base_text)

		return self.__parsed_text



	
