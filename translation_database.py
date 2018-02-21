import sqlite3

class TranslationDatabase:
	#TODO: INDICES
	#sentence table should have joint primary key (or at least unique/indexed by)
	#article ID, sentence #, language

	database_name = 'translations.db'
	article_table_name = 'articles'
	article_table_schema = 'id INTEGER PRIMARY KEY, base_text TEXT'
	sentence_table_name = 'sentences'
	sentence_table_schema = 'id INTEGER PRIMARY KEY, sentence_number INTEGER, base_text TEXT, language TEXT, article_id INTEGER, FOREIGN KEY(article_id) REFERENCES articles(id)'

	def __init__(self):
		self.db = sqlite3.connect(self.database_name)

	def init_db(self):
		self.create_table(self.article_table_name, self.article_table_schema)
		self.create_table(self.sentence_table_name, self.sentence_table_schema)

	def create_table(self, table_name, schema):
		c = self.db.cursor()
		c.execute("PRAGMA foreign_keys = ON;")
		c.execute('CREATE TABLE ' + table_name + ' (' + schema + ');')



