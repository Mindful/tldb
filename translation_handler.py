import translation_client
import translation_database
import spacy
import sentence


class ContentNotFoundException(Exception):
    pass


class TranslationHandler:

    languages = ['ja']

    def __init__(self, logger):
        self.db = translation_database.TranslationDatabase()
        self.web_client = translation_client.TranslationClient()
        self.logger = logger


    def register_content(self, text, external_id, source):
        content = self.db.create_content(text, external_id, source)
        for language in self.languages:
            self.__save_content_translations(content, language)


    def __save_content_translations(self, content, language):
        output_sentence_tuples = []
        for counter, sentence in enumerate(content.get_parsed_text().sents):
            sentence_number = counter + 1 # Counter starts from 0
            sentence_translation = self.web_client.translate(sentence.text, language)
            output_sentence_tuples.append((sentence_number, sentence_translation, language, content.db_id))

        return self.db.create_sentences(output_sentence_tuples)


    def get_sentence(self, content_external_id, content_source, sentence_number, language):
        content = self.db.get_content(content_source, content_external_id)
        if not content:
            raise ContentNotFoundException()

        sentence = self.db.get_sentence(content_external_id, language, sentence_number)
        if not sentence:
            self.logger.info("No pretranslated sentence found for content ID ", content_external_id, " language ", language, " sentence number ",
                sentence_number, ". Translating and returning.")
            sentence_text = list(content.get_parsed_text())[sentence_number].text
            sentence_translation = self.web_client.translate(sentence.text, language)
            return self.db.create_sentence(sentence_number, sentence_translation, language, content.db_id)









