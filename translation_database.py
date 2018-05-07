import sqlite3
import article

class TranslationDatabase:
	#TODO: INDICES
	#sentence table should have joint primary key (or at least unique/indexed by)
	#article ID, sentence #, language

	#Probably have this index with current primary key setup (confirm that). see if we need any single indexes - I don't think we will though
	#TODO: does the ordering of the primary key attributes matter? is it right? it might influence the index construction
	#specifically, we might want to get all the sentences for an article with a given language (hopefully current order is good for that)

	database_name = 'translations.db'
	article_table_name = 'articles'
	article_table_schema = 'id INTEGER PRIMARY KEY AUTOINCREMENT, base_text TEXT UNIQUE'
	sentence_table_name = 'sentences'
	sentence_table_schema = 'sentence_number INTEGER, translated_text TEXT, language TEXT, article_id INTEGER, FOREIGN KEY(article_id) REFERENCES articles(id), PRIMARY KEY(article_id, language, sentence_number)'

	def __init__(self):
		self.db = sqlite3.connect(self.database_name)

	def init_db(self):
		self.create_table(self.article_table_name, self.article_table_schema)
		self.create_table(self.sentence_table_name, self.sentence_table_schema)

	def create_table(self, table_name, schema):
		c = self.db.cursor()
		c.execute("PRAGMA foreign_keys = ON;")
		c.execute('CREATE TABLE ' + table_name + ' (' + schema + ');')

	def create_article(self, article_text):
		c = self.db.cursor()
		c.execute("INSERT INTO " + self.article_table_name + " (base_text) VALUES (?)", (article_text,))
		self.db.commit()
		return Article(c.lastrowid, article_text)



