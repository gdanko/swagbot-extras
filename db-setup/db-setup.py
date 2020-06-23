#!/usr/bin/env python3

import logging
import os
import re
import sqlite3

def configure_logger():
	logger = logging.getLogger()
	handler = logging.StreamHandler()
	formatter = logging.Formatter("%(levelname)s %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	logger.propagate = False
	return logger

def is_file(path):
	try:
		if os.path.isfile(path):
			return True
		else:
			return False
	except:
		return False
	return False

def populate_quotes(file=None, category=None):
	if is_file(file):
		logger.info("Populating the quotes table with {} quotes.".format(category))
		delete = "DELETE FROM quotes WHERE category='{}'".format(category)
		cursor.execute(delete)
		conn.commit()

		with open(file) as lines:
			for quote in lines:
				quote = quote.rstrip()
				insert = "INSERT INTO quotes (category,quote) VALUES(?,?)"
				cursor.execute(insert, (
					category,
					quote,
				))
				conn.commit()
	else:
		logger.warn("Could not add {} quotes because {} not found.".format(category, file))

def populate_currency_table():
	file = "./currency-symbols.txt"
	if is_file(file):
		logger.info("Populating the currency conversion table.")
		cursor.execute("DELETE FROM currency_conversion")
		with open(file) as lines:
			for line in lines:
				line = line.rstrip()
				symbol,nation = re.split("\s*,\s*", line)
				insert = "INSERT INTO currency_conversion (nation,symbol) VALUES(?,?)"
				cursor.execute(insert, (
					nation,
					symbol
				))
				conn.commit()
	else:
		logger.warn("Could not populate the currency symbols table because {} not found.".format(file))

def populate_graffin_table():
	file = "./graffin.txt"
	if is_file(file):
		logger.info("Populating the graffin table.")
		cursor.execute("DELETE FROM graffin")
		with open(file) as lines:
			for line in lines:
				line = line.rstrip()
				word,definition = re.split("\s*\|\s*", line)
				insert = "INSERT INTO graffin (word,definition) VALUES(?,?)"
				cursor.execute(insert, (
					word,
					definition.capitalize()
				))
				conn.commit()
	else:
		logger.warn("Could not populate the currency symbols table because {} not found.".format(file))

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

logger = configure_logger()
#dbfile = "{}/data/extras.db".format(PACKAGE_ROOT)
dbfile = "../data/extras.db"
conn = sqlite3.connect(dbfile, check_same_thread=False)
cursor = conn.cursor()

populate_quotes(file="./baracus-quotes.txt", category="baracus")
populate_quotes(file="./kim-quotes.txt", category="kim")
populate_quotes(file="./fortunes.txt", category="fortune")
populate_quotes(file="./yomama-quotes.txt", category="yomama")
populate_currency_table()
populate_graffin_table()
