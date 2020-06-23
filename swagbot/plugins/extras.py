from pprint import pprint, pformat
from swagbot.core import BasePlugin
from urllib.parse import urlencode
import argparse
import os
import pint
import random
import re
import swagbot.extras_database as db
import swagbot.request as request
import swagbot.utils as utils
import sys
import time

class Plugin(object):
	def __init__(self, bot):
		self.__configure_parsers()
		self.methods = self.__setup_methods()
		BasePlugin.__init__(self, bot)

		self.bitly_key = self.bot.config["keys"]["bitly"] if "bitly" in self.bot.config["keys"] else None
		self.geonames_key = self.bot.config["keys"]["geonames"] if "geonames" in self.bot.config["keys"] else None
		self.wordnik_key = self.bot.config["keys"]["wordnik"] if "wordnik" in self.bot.config["keys"] else None
		self.yelp_key = self.bot.config["keys"]["yelp"] if "yelp" in self.bot.config["keys"] else None

	def ball(self, command=None):
		if command:
			question = command.command_args
			if question:
				answers = [
					"It is certain",
					"It is decidedly so",
					"Without a doubt",
					"Yes, definitely",
					"You may rely on it",
					"As I see it, yes",
					"Most likely",
					"Outlook good",
					"Yes",
					"Signs point to yes",
					"Reply hazy, try again",
					"Ask again later",
					"Better not tell you now",
					"Cannot predict now",
					"Concentrate and ask again",
					"Don't count on it",
					"My reply is no",
					"My sources say no",
					"Outlook not so good",
					"Very doubtful"
				]
				answer = random.choice(answers)
				utils.make_success(command, content=answer)
			else:
				utils.make_error(command, content=["No question specified.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def apg(self, command=None):
		if command:
			sys.argv = command.argv
			try:
				args = self.apg_parser.parse_args()
			except:
				utils.make_error(command, content=["Invalid input received.", self.apg_parser.format_help().rstrip()])
				return

			letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			numbers = "0123456789"
			symbols = "!@#$%^&*()_+-={}|[]\:\";\'<>?,./"

			characters = []
			characters += list(letters.upper())
			characters += list(letters.lower())
			characters += list(numbers)

			length = int(args.length)
			quantity = int(args.quantity)

			if (quantity <= 0) or (quantity > 10):
				quantity = 10
			passwords = []
			for x in range(0, quantity):
				passwords.append("".join(random.choice(characters) for x in range(length)))
			utils.make_success(command, content=passwords)
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def baracus(self, command=None):
		if command:
			quote = db.quotes(category="baracus")
			if quote:
				utils.make_success(command, content=quote)
			else:
				utils.make_error(command, content="Failed to find a quote. :(")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def bytes(self, command=None):
		if command:
			sys.argv = command.argv
			try:
				args = self.bytes_parser.parse_args()
			except:
				print(1)
				utils.make_error(command, content=["Invalid input received.", self.bytes_parser.format_help().rstrip()])
				return

			pattern = r"^([0-9]+)([a-zA-Z]+)$"
			matches = re.findall(pattern, args.base)
			if matches and len(matches) == 1:
				if len(matches[0]) == 2:
					(amount, unit) = matches[0]
					amount = int(amount)
					unit = unit.lower()
					units = ["bytes", "k", "m", "g", "t", "p", "e"]
					all_units = ["bytes", "k", "m", "g", "t", "p", "e", "kb", "mb", "gb", "tb", "pb", "eb"] 
					base = 1024
					if unit in all_units:
						if unit != "bytes":
							unit = unit[0][0]
					out = []
					bit = None
					byte = None
					conversion_table = {
						"bytes": {"mult": 0, "display": "bytes"},
						"k": {"mult": 1, "display": "KiB"},
						"m": {"mult": 2, "display": "MiB"},
						"g": {"mult": 3, "display": "GiB"},
						"t": {"mult": 4, "display": "TiB"},
						"p": {"mult": 5, "display": "PiB"},
						"e": {"mult": 6, "display": "EiB"},
					}
					bit = int((amount * (base ** conversion_table[unit]["mult"]) * 8))
					byte = int(bit / 8)
					out.append("{:.1f} bits".format(bit))

					for key in units:
						if key != unit:
							multiplier = conversion_table[key]["mult"]
							converted = "{:.15f}".format(byte / (base ** multiplier))
							i, d = re.split(r"\.\s*", str(converted))
							if int(i) > 0:
								converted = "{:.1f}".format(float(i))
							elif int(d) == 0:
								converted = int(converted)
						
							if float(converted) > 0:
								out.append("{} {}".format(converted, conversion_table[key]["display"]))
					utils.make_success(command, content="{} {} = {}".format(amount, conversion_table[unit]["display"], ", ".join(out)))
				else:
					utils.make_error(command, content=["Invalid input received.", self.bytes_parser.format_help().rstrip()])
			else:
				utils.make_error(command, content=["Invalid input received.", self.bytes_parser.format_help().rstrip()])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def calc(self, command=None):
		if command:
			equation = command.command_args
			if args.equation:
				answer = os.popen("echo '{}' | bc".format(equation)).read().rstrip()
				utils.make_success(command, content="{} = {}".format(equation, answer))
			else:
				utils.make_error(command, content=["No input received.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def currency(self, command=None):
		# List all currencies
		# https://free.currencyconverterapi.com/api/v5/currencies
		# Compact output
		# https://free.currencyconverterapi.com/api/v5/convert?q=USD_PHP&compact=y
		# Compact more
		# https://free.currencyconverterapi.com/api/v5/convert?q=USD_PHP&compact=ultra
		if command:
			sys.argv = command.argv
			try:
				args = self.currency_parser.parse_args()
			except:
				utils.make_error(command, content=["Invalid input received.", self.currency_parser.format_usage().rstrip()])
				return

			from_symbol = getattr(args, "from").upper()
			to_symbol = getattr(args, "to").upper()
			from_amount = args.amount

			if re.search("^[A-Za-z]{3}$", from_symbol):
				from_symbol = from_symbol
			else:
				fs = db.get_currency_symbol(nation=from_symbol)
				if fs:
					from_symbol = fs["symbol"]
				else:
					utils.make_error(command, content="Could not find the currency symbol for {}.".format(from_symbol))
					return

			if re.search("^[A-Za-z]{3}$", to_symbol):
				to_symbol = to_symbol
			else:
				fs = db.get_currency_symbol(nation=to_symbol)
				if fs:
					to_symbol = fs["symbol"]
				else:
					utils.make_error(command, content="Could not find the currency symbol for {}.".format(from_symbol))
					return

			conversion = "{}_{}".format(from_symbol, to_symbol)
			uri = "http://free.currencyconverterapi.com/api/v5/convert?q={}&compact=ultra".format(conversion)
			request.get(self, uri=uri)
			if self.success:
				if conversion in self.response:
					to_amount = float(from_amount) * float(self.response[conversion])
					utils.make_success(command, content="{:.2f} {} = {:.2f} {}".format(
						float(from_amount),
						from_symbol,
						float(to_amount),
						to_symbol,
					))
				else:
					utils.make_error(command, content="Failed to convert the currency.")
			else:
				utils.make_error(command, content="Failed to convert the currency.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def dict(self, command=None):
		if command:
			if self.wordnik_key:
				word = command.command_args
				if word:
					limit = 3
					uri = "http://api.wordnik.com/v4/word.json/{}/definitions?api_key={}&includeRelated=false&includeTags=false&limit={}&sourceDictionaries=all&useCanonical=false".format(word, self.wordnik_key, limit)
					request.get(self, uri=uri)
					if self.success:
						if len(self.response["body"]) > 0:
							messages = []
							for d in self.response["body"]:
								messages.append("{}: {}: {}".format(word, d["partOfSpeech"], d["text"]))
							utils.make_success(command, content=messages)
						else:
							utils.make_error(command, content="Unable to fetch the dictionary definition.")
					else:
						utils.make_error(command, content="Unable to fetch the dictionary definition.")
				else:
					utils.make_error(command, content=["No word specified.", "Usage: {}".format(command.command["usage"])])
			else:
				utils.make_error(command, content="Cannot perform the command at this time.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def fortune(self, command=None):
		if command:
			fortune = db.quotes(category="fortune")
			if fortune:
				utils.make_success(command, content=fortune)
			else:
				utils.make_error(command, content="Failed to find a fortune. :(")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def graffin(self, command=None):
		if command:
			graffin = db.graffin()
			if graffin:
				utils.make_success(command, content="{}: {}".format(graffin["word"], graffin["definition"]))
			else:
				utils.make_error(command, content="Oops! I was not able to find any available Greg Graffin words.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def kim(self, command=None):
		if command:
			quote = db.quotes(category="kim")
			if quote:
				utils.make_success(command, content=quote)
			else:
				utils.make_error(command, content="Failed to find a quote. :(")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def stocks(self, command=None):
		#https://api.iextrading.com/1.0/stock/aapl/quote
		if command:
			symbols = command.command_args
			if symbols:
				symbols = re.split(",", symbols)
				messages = []
				for symbol in symbols:
					request.get(self, uri="https://api.iextrading.com/1.0/stock/{}/quote".format(symbol))
					if self.success:
						messages.append(
							"{} - Price: ${} | Open: ${} | Low: ${} | High: ${} | Percent change: {}%".format(
								self.response["symbol"],
								self.response["delayedPrice"],
								self.response["open"],
								self.response["high"],
								self.response["low"],
								self.response["changePercent"],
						))
					else:
						messages.append("Symbol {} not found".format(symbol))
				utils.make_success(command, content=messages)
			else:
				utils.make_error(command, content=["No symbols specified.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def tiny(self, command=None):
		if command:
			if self.bitly_key:
				if url:
					url = command.command_args
					url = re.sub("^\<", "", url)
					url = re.sub("\>$", "", url)
					if utils.validate_url(url) == True:
						uri = "https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}".format(self.bitly_key, url)
						request.get(self, uri=uri)
						if self.success:
							if "status_code" in self.response:
								if self.response["status_code"] == 200:
									if self.response["status_txt"].lower() == "ok":
										utils.make_success(command, content=self.response["data"]["url"])
									elif self.response["status_txt"].lower() == "already_a_bitly_link":
										utils.make_error(command, content="You cannot shorten a shortened link.")
									else:
										utils.make_error(command, content="The URL shortener returned an error: {}.".format(self.response["status_txt"]))
						else:
							utils.make_error(command, content="An unknown error has occurred.")
					else:
						utils.make_error(command, content="You specified an invalid URL.")
				else:
					utils.make_error(command, content=["No URL specified.", "Usage: {}".format(command.command["usage"])])
			else:
				utils.make_error(command, content="Cannot perform the command at this time.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def udict(self, command=None):
		if command:
			phrase = command.command_args
			if phrase:
				uri = "http://api.urbandictionary.com/v0/define?term={}".format(phrase)
				request.get(self, uri=uri)
				if self.success:
					if "list" in self.response:
						if len(self.response["list"]) > 0:
							utils.make_success(command, content="{}: {}".format(phrase, self.response["list"][0]["definition"]))
						else:
							utils.make_error(command, content="Definition for {} not found on Urban Dictionary.".format(phrase))
					else:
						utils.make_error(command, content="Definition for {} not found on Urban Dictionary.".format(phrase))
				else:
					utils.make_error(command, content="Definition for {} not found on Urban Dictionary.".format(phrase))
			else:
				utils.make_error(command, content=["No phrase specified.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def units(self, command=None):
		if command:
			opts = command.command_args
			if opts:
				pattern = r"^([-+]?[0-9]*\.?[0-9]+)\s+([a-zA-Z0-9^]+)\s+([a-zA-Z0-9^]+)$"
				matches = re.findall(pattern, opts)
				if matches and len(matches) == 1:
					if len(matches[0]) == 3:
						(u, f, t) = matches[0]
						ureg = pint.UnitRegistry()
						try:
							converted = ureg.Quantity(float(u), ureg.parse_expression(f)).to(t)._magnitude
							utils.make_success(command, content="{:.2f} {} = {:.2f} {}".format(float(u), f, float(converted), t))
						except:
							utils.make_error(command, content="Conversion failed.")
					else:
						utils.make_error(command, content=["Invalid input.", "Usage: {}".format(command.command["usage"])])
				else:
					utils.make_error(command, content=["Invalid input.", "Usage: {}".format(command.command["usage"])])
			else:
				utils.make_error(command, content=["No input received.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def weather(self, command=None):
		if command:
			location = command.command_args
			if location:
				uri = "https://query.yahooapis.com/v1/public/yql?format=json&q=select woeid from geo.places where text='{}' limit 1".format(location)
				request.get(self, uri=uri)
				if self.success:
					woeid = self.response["query"]["results"]["place"]["woeid"]
					uri = "https://query.yahooapis.com/v1/public/yql?format=json&q=select * from weather.forecast where woeid={}".format(woeid)
					request.get(self, uri=uri)
					if self.success:
						max_forecast_days = 5
						messages = []
						condition = self.response["query"]["results"]["channel"]["item"]["condition"]
						current_condition = condition["text"]
						current_f = condition["temp"]
						current_c = utils.farenheit_to_celsius(current_f)

						messages.append("Currently {}°F ({}°C) and {}.".format(current_f, int(current_c), current_condition))
						forecast = self.response["query"]["results"]["channel"]["item"]["forecast"]
						num_days = len(forecast) if len(forecast) >= max_forecast_days else len(forecast)
						for i, daily_forecast in enumerate(forecast):
							if i == 0:
								daily_forecast["date"] += " (Today)"

							if i <= (max_forecast_days - 1):
								high_f = daily_forecast["high"]
								high_c = utils.farenheit_to_celsius(high_f)
								low_f = daily_forecast["low"]
								low_c = utils.farenheit_to_celsius(low_f)
								messages.append("{} - High: {}°F ({}°C) | Low: {}°F ({}°C)".format(daily_forecast["date"], high_f, int(high_c), low_f, int(low_c)))
						utils.make_success(command, content=messages)
					else:
						utils.make_error(command, "Failed to fetch weather data.")
				else:
					utils.make_error(command, "Could not find the WOEID for {}.".format(location))
			else:
				utils.make_error(command, content=["No location specified.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def yelp(self, command=None):
		if command:
			if self.yelp_key:
				sys.argv = command.argv
				try:
					args = self.yelp_parser.parse_args()
				except:
					utils.make_error(command, content=["Invalid input received.", self.yelp_parser.format_help().rstrip()])
					return

				# I need to make a Yelp module
				qs = {}
				qs["term"] = args.term
				qs["location"] = args.location
				if args.categories: qs["categories"] = args.categories
				if args.price:
					price_map = {"$": "1", "$$": "2", "$$$": "3", "$$$$": "4"}
					qs["price"] = ",".join([price_map[p] for p in re.split(r"\s*,\s*", args.price)])

				self.response = {}
				uri = "https://api.yelp.com/v3/businesses/search?{}".format("&".join([ urlencode({k: str(v)}) for k, v in qs.items() ]))
				headers = {"Authorization": "Bearer {}".format(self.yelp_key)}
				request.get(self, uri=uri, extra_headers=headers)
				if self.success:
					rating = float(args.rating) if args.rating else 1.0
					results = [b for b in self.response["businesses"] if b["rating"] >= rating]
					if len(results) > 0:
						messages = []
						formatter = "{:30}{:18}{:50}{:<10}{:<8}{:8}{:25}"
						header = formatter.format("Name", "Phone", "Address", "Reviews", "Rating", "Price", "Yelp URL")
						divider = "=" * len(header)
						messages.append(header)
						messages.append(divider)
						for business in results:
							messages.append(formatter.format(
								business["name"][0:27],
								business["display_phone"],
								", ".join(business["location"]["display_address"])[0:47],
								business["review_count"],
								business["rating"],
								business["price"],
								self.__tiny_url(url=business["url"]),

							))
						utils.make_success(command, content=messages)
					else:
						utils.make_success(command, content="No results found matching the specified criteria.")
				else:
					self.bot.logger.error(pformat(self.response))
					utils.make_error(command, content="An error occurred while connecting to Yelp.")
			else:
				utils.make_error(command, content="Cannot perform the command at this time.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def yomama(self, command=None):
		if command:
			joke = db.quotes(category="yomama")
			if joke:
				utils.make_success(command, content=joke)
			else:
				utils.make_error(command, content="Failed to find a joke. :(")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def zip(self, command=None):
		if command:
			if self.geonames_key:
				opts = command.command_args
				if opts:
					state = None
					bits = re.split(r"\s*,\s*", str(opts))
					if len(bits) == 3:
						(city,state,country) = bits
						if country.lower() != "us":
							utils.make_error(command, content="You may only specify a state when the country is US.")
							return
					elif len(bits) == 2:
						(city,country) = bits
					else:
						utils.make_error(command, content="You must minimally specify country and city.")
						return

					zips = []
					batch_size = 32
					uri = "http://api.geonames.org/postalCodeSearchJSON?placename={}&country={}&username={}&maxRows=200".format(city, country, self.geonames_key)
					request.get(self, uri=uri)
					if self.success:
						if "postalCodes" in self.response:
							if len(self.response["postalCodes"]) > 0:
								if state:
									zips = [x["postalCode"] for x in self.response["postalCodes"] if state.lower() == x["adminCode1"].lower()]
								else:
									zips = [x["postalCode"] for x in self.response["postalCodes"]]
								utils.make_success(command, content=", ".join(sorted(zips)))
							else:
								utils.make_error(command, content="Location not found in postal code data.")
						else:
							utils.make_error(command, content="Failed to fetch postal code data.")
					else:
						utils.make_error(command, content="Failed to fetch postal code data.")
				else:
					utils.make_error(command, content=["No location specified.", "Usage: {}".format(command.command["usage"])])
			else:
				utils.make_error(command, content="Cannot perform the command at this time.")
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def __tiny_url(self, url=None):
		if self.bitly_key:
			uri = "https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}".format(self.bitly_key, url)
			request.get(self, uri=uri)
			if self.success:
				if "status_code" in self.response:
					if self.response["status_code"] == 200:
						if self.response["status_txt"].lower() == "ok":
							return self.response["data"]["url"]
			else:
				pprint(self.response)
				return url
		else:
			return url

	def __configure_parsers(self):
		self.apg_parser = argparse.ArgumentParser(add_help=False, prog="apg")
		self.apg_parser.add_argument("-l", "--length", help="The length of the generated password.", required=True, type=int),
		self.apg_parser.add_argument("-q", "--quantity", help="The number of passwords to generate.", required=True, type=int)

		self.bytes_parser = argparse.ArgumentParser(add_help=False, prog="bytes")
		self.bytes_parser.add_argument("-b", "--base", help="Base amount for conversion, without spaces, e.g. 100GB, 1 TB", required=True)

		self.currency_parser = argparse.ArgumentParser(add_help=False, prog="currency")
		self.currency_parser.add_argument("-a", "--amount", help="The amount of the 'from' currency.", required=True),
		self.currency_parser.add_argument("-f", "--from", help="The nation or symbol of the 'from' currency.", required=True)
		self.currency_parser.add_argument("-t", "--to", help="The nation or symbol of the 'to' currency.", required=True)

		self.starwars_parser = argparse.ArgumentParser(add_help=False, prog="starwars")
		self.starwars_parser.add_argument("--film", help="Search for a film.", required=False),
		self.starwars_parser.add_argument("--person", help="Search for a character.", required=False)
		self.starwars_parser.add_argument("--planet", help="Search for a planet.", required=False)
		self.starwars_parser.add_argument("--species", help="Search for a species.", required=False)
		self.starwars_parser.add_argument("--starship", help="Search for a starship.", required=False)
		self.starwars_parser.add_argument("--vehicle", help="Search for a vehicle.", required=False)

		self.yelp_parser = argparse.ArgumentParser(add_help=False, prog="yelp")
		self.yelp_parser.add_argument("-t", "--term", help="Search term (e.g. 'food', 'restaurants')", required=True)
		self.yelp_parser.add_argument("-l", "--location", help="Address, neighborhood, city, state, or zip.", required=True),
		self.yelp_parser.add_argument("-c", "--categories", help="The category filter can be a list of comma delimited categories.", required=False)
		self.yelp_parser.add_argument("-p", "--price", help="Any combination of $,$$,$$$,$$$$.", required=False)
		self.yelp_parser.add_argument("-r", "--rating", help="Specify minimum rating level.", required=False)

	def __setup_methods(self):
		return {
			"8ball": {
				"usage": "8ball <question> -- Ask the 8ball a question.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"method": "ball",
				"hidden": 0,
				"monospace": 0
			},
			"apg": {
				"usage": self.apg_parser.format_help().rstrip(),
				"level": 0,
				"type": "private",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 1
			},
			"baracus": {
				"usage": "baracus -- Enjoy a quote from BA Baracus.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"bytes": {
				"usage": self.bytes_parser.format_help().rstrip(),
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 1
			},
			"calc": {
				"usage": "calc <input> -- Calculate input via bc(1)",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"currency": {
				"usage": self.currency_parser.format_help().rstrip(),
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"dict": {
				"usage": "dict <word> -- Look up <word> in an online dictionary.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"fortune": {
				"usage": "fortune -- Display a Unix fortune.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"graffin": {
				"usage": "graffin -- Greg Graffin is probably smarter than you are. See a random word from one of his songs along with its definition.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"kim": {
				"usage": "kim -- Display a nugget of wisdom from Kim Jong-un.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"stocks": {
				"usage": "stocks <symbol>,<symbol> -- Display basic stock quote information for upto 5 <symbol>s.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"tiny": {
				"usage": "tiny <url> -- Shorten a URL.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0
			},
			"udict": {
				"usage": "udict <phrase> -- Look up <phrase> on Urban Dictionary.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"units": {
				"usage": "units <number> <from> <to> -- Unit converter, converts <from> <number> to <to>. Example: units 5 ft mm.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"weather": {
				"usage": "weather <location> -- Display weather conditions for <location> where <location> is one of city, US ZIP or Canadian postal code.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
			"yelp": {
				"usage": self.yelp_parser.format_help().rstrip(),
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 1,
				"monospace": 1
			},
			"yomama": {
				"usage": "yomama - Tell a (sometimes) funny yo mama joke.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 1,
				"monospace": 0
			},
			"zip": {
				"usage": "zip <country>,<city>,[<state>] -- Display postal codes for a given location. <country> must be the a valid country code and <city> can be a city name or city,state combination. Example: zip IN, Bangalore",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"monospace": 0
			},
		}