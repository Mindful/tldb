import translation_client
import translation_database
import logging


class ContentNotFoundException(Exception):
    pass

class SentenceNotFoundException(Exception):
    pass


class TranslationHandler:

    #We will automatically generate translations for any languages in this array upon article submission. Intentionally empty 
    default_translation_languages = []

    def __init__(self):
        self.db = translation_database.TranslationDatabase()
        self.web_client = translation_client.TranslationClient()
        self.logger = logging.getLogger()

    def register_content(self, text, external_id, source):
        preexisting_content = self.db.get_content(source, external_id)
        if preexisting_content:
            self.logger.info("Replacing pre-existing content with external ID %s and source %s", external_id, source)
            self.db.delete_sentences_for_content(preexisting_content)
        else:
            self.logger.info("Creating content with external ID %s and source %s", external_id, source)

        content = self.db.upsert_content(text, external_id, source)
        for language in self.default_translation_languages:
            self.__save_content_translations(content, language)


        return content

    def delete_content(self, external_id, source):
        content = self.db.get_content(source, external_id)
        if content:
            self.db.delete_sentences_for_content(content)
            self.db.delete_content(content)
            return content
        else:
            raise ContentNotFoundException()


    def get_content(self, content_external_id, content_source):
        content = self.db.get_content(content_source, content_external_id)
        if not content:
            raise ContentNotFoundException()
        else:
            return content


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

        sentence = self.db.get_sentence(content.db_id, language, sentence_number)
        if sentence:
            return sentence
        else:
            sentences = list(content.get_parsed_text().sents)
            if sentence_number >= len(sentences):
                raise SentenceNotFoundException()
            
            self.logger.info("No pretranslated sentence found for content ID %s, language \"%s\", and sentence number %d."
                             " Translating and returning.", content_external_id, language, sentence_number)
            sentence_text = sentences[sentence_number].text
            sentence_translation = self.web_client.translate(sentence_text, language)
            return self.db.create_sentence(sentence_number, sentence_translation, language, content.db_id)










