import sqlite3
import content
import sentence
import logging

class TranslationDatabase:
    #TODO: INDICES
    #sentence table should have joint primary key (or at least unique/indexed by)
    #content ID, sentence #, language

    #Probably have this index with current primary key setup (confirm that). see if we need any single indexes - I don't think we will though
    #TODO: does the ordering of the primary key attributes matter? is it right? it might influence the index construction
    #specifically, we might want to get all the sentences for an content with a given language (hopefully current order is good for that)

    database_name = 'translations.db'
    content_table_name = 'contents'
    content_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, base_text TEXT UNIQUE, external_id INTEGER, data_source TEXT, UNIQUE (external_id, data_source)'
    sentence_table_name = 'sentences'
    sentence_table_schema = 'sentence_number INTEGER, translated_text TEXT, language TEXT, content_id INTEGER, FOREIGN KEY(content_id) REFERENCES contents(id), PRIMARY KEY(content_id, language, sentence_number)'

    def __init__(self):
        self.db = sqlite3.connect(self.database_name)
        self.init_db()
        self.logger = logging.getLogger()

    def __get_cursor(self):
        return self.db.cursor()

    def init_db(self):
        self.create_table(self.content_table_name, self.content_table_schema)
        self.create_table(self.sentence_table_name, self.sentence_table_schema)

    def create_table(self, table_name, schema):
        c = self.__get_cursor()
        c.execute("PRAGMA foreign_keys = ON;")
        c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (' + schema + ');')

    def upsert_content(self, content_text, external_id, data_source):
        c = self.__get_cursor()
        c.execute("INSERT OR REPLACE INTO " + self.content_table_name + " (base_text, external_id, data_source) VALUES (?,?,?)", (content_text,external_id,data_source))
        self.db.commit()
        return content.Content(c.lastrowid, content_text, external_id, data_source)

    def create_sentences(self, sentence_tuple_list):
        c = self.__get_cursor()
        c.executemany("INSERT INTO " + self.sentence_table_name + " VALUES (?,?,?,?)", sentence_tuple_list)
        self.db.commit()
        return [sentence.Sentence(*x) for x in sentence_tuple_list]

    def create_sentence(self, sentence_number, translated_text, language, content_id):
        return self.create_sentences([(sentence_number, translated_text, language, content_id)])[0]

    def delete_sentences_for_content(self, content):
        content_id = content.db_id
        c = self.__get_cursor()
        c.execute("DELETE FROM " + self.sentence_table_name + " WHERE content_id=?", (content_id,))
        self.db.commit()


    def get_content(self, source, external_id):
        c = self.__get_cursor()
        c.execute("SELECT * FROM " + self.content_table_name + " WHERE external_id=? AND data_source=?", (external_id, source))
        content_data = c.fetchone()
        if content_data:
            return content.Content(*content_data)
        else:
            return None

    def get_sentence(self, content_id, language, sentence_number):
        c = self.__get_cursor()
        c.execute("SELECT * FROM " + self.sentence_table_name + " WHERE content_id=? and language=? and sentence_number=?", (content_id, language, sentence_number))
        sentence_data = c.fetchone()
        if sentence_data:
            return sentence.Sentence(*sentence_data)
        else:
            return None





