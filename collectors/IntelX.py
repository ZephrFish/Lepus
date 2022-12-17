import requests
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	IX = []

	print(colored("[*]-Searching IntelX...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	INTELX_API_KEY = parser.get("IntelX", "INTELX_API_KEY")
	INTELX_URL = parser.get("IntelX", "INTELX_URL")

	if INTELX_API_KEY == "" or INTELX_URL == "":
		print("  \__", colored("No IntelX API key or URL configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		params = {"Term": domain, "Maxresults": 100000, "Media": 0, "Target": 1, "Timeout": 20}
		url = "{0}phonebook/search?k={1}".format(INTELX_URL, INTELX_API_KEY)

		try:
			response = requests.post(url, headers=headers, json=params)
			searchID = loads(response.text)["id"]

			url = "{0}phonebook/search/result?k={1}&id={2}&limit=100000".format(INTELX_URL, INTELX_API_KEY, searchID)
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				IX.extend(results)
				IX = set(IX)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(IX), "yellow")))
			return IX

		except requests.exceptions.RequestException as err:
			print("  \__", colored(err, "red"))
			return []

		except requests.exceptions.HTTPError as errh:
			print("  \__", colored(errh, "red"))
			return []

		except requests.exceptions.ConnectionError as errc:
			print("  \__", colored(errc, "red"))
			return []

		except requests.exceptions.Timeout as errt:
			print("  \__", colored(errt, "red"))
			return []
		
		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return []