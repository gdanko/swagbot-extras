/* sqlite3 ../swagbot/data/extras.db < schema.sql */

DROP TABLE IF EXISTS currency_conversion;
CREATE TABLE currency_conversion (
	nation TEXT NOT NULL,
	symbol TEXT NOT NULL
);

DROP TABLE IF EXISTS graffin;
CREATE TABLE graffin (
    word TEXT NOT NULL PRIMARY KEY UNIQUE,
    definition TEXT NOT NULL
);

DROP TABLE IF EXISTS quotes;
CREATE TABLE quotes (
	quote TEXT NOT NULL,
	category TEXT NOT NULL
);
