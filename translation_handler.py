import translation_client
import translation_database
import logging


class ContentNotFoundException(Exception):
    pass


class TranslationHandler:

    languages = ['ja']

    def __init__(self):
        self.db = translation_database.TranslationDatabase()
        self.web_client = translation_client.TranslationClient()
        self.logger = logging.getLogger()

    def register_content(self, text, external_id, source):
        content = self.db.create_content(text, external_id, source)
        for language in self.languages:
            self.__save_content_translations(content, language)


    def __save_content_translations(self, content, language):
        output_sentence_tuples = []
        for counter, sentence in enumerate(content.get_parsed_text().sents):
            sentence_number = counter
            sentence_translation = self.web_client.translate(sentence.text, language)
            output_sentence_tuples.append((sentence_number, sentence_translation, language, content.db_id))

        return self.db.create_sentences(output_sentence_tuples)

    def get_sentence(self, content_external_id, content_source, sentence_number, language):
        content = self.db.get_content(content_source, content_external_id)
        if not content:
            raise ContentNotFoundException()

        sentence = self.db.get_sentence(content_external_id, language, sentence_number)
        if sentence:
            return sentence
        else:
            self.logger.info("No pretranslated sentence found for content ID %d, language \"%s\", and sentence number %d."
                             " Translating and returning.", content_external_id, language, sentence_number)
            sentence_text = list(content.get_parsed_text().sents)[sentence_number].text
            sentence_translation = self.web_client.translate(sentence_text, language)
            return self.db.create_sentence(sentence_number, sentence_translation, language, content.db_id)










