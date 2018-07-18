import spacy

class Content:

    #Only using sentencizing right now, so for speed we can disable the other parts of spacy
    nlp = spacy.load('en', disable=['tagger', 'parser', 'ner', 'textcat'])
    nlp.add_pipe(nlp.create_pipe("sentencizer"))

    def __init__(self, db_id, base_text, external_id, data_source):
        self.db_id = db_id
        self.base_text = base_text
        self.external_id = external_id
        self.data_source = data_source
        self.__parsed_text = None
        self.__sent_end_map = None


    def get_parsed_text(self):
        if not self.__parsed_text:
            self.__parsed_text = self.nlp(self.base_text)

        return self.__parsed_text

    def get_sentence_endings_map(self):
        if not self.__sent_end_map:
            sent_end_map = {}
            parsed_text = self.get_parsed_text()
            for index,sentence in enumerate(parsed_text.sents):
                sent_end_map[index] = len(str(parsed_text[0:sentence.end]))

            self.__sent_end_map = sent_end_map

        return self.__sent_end_map

