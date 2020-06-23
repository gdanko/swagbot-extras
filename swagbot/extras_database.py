import os
import sqlite3

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

def graffin():
	select = "SELECT * FROM graffin ORDER BY RANDOM() LIMIT 1"
	cursor.execute(select)
	result = cursor.fetchone()
	return result if result else None

def quotes(category=None):
	select = "SELECT * FROM quotes WHERE category='{}' ORDER BY RANDOM() LIMIT 1".format(category)
	cursor.execute(select)
	result = cursor.fetchone()
	return result["quote"] if result else None	

def get_currency_symbol(nation=None):
	select = "SELECT * FROM currency_conversion WHERE nation='{}' COLLATE NOCASE".format(nation)
	cursor.execute(select)
	result = cursor.fetchone()
	return result if result else None

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

dbfile = "{}/data/extras.db".format(PACKAGE_ROOT)
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()