import requests
from time import sleep
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	US = []

	print(colored("[*]-Searching URLScan...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	URLSCAN_API_KEY = parser.get("URLScan", "URLSCAN_API_KEY")

	if URLSCAN_API_KEY == "":
		print("  \__", colored("No URLScan API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "Api-Key": URLSCAN_API_KEY}
		quotaUrl = "https://urlscan.io/user/quotas/"
		size = 1000
		itemsInResponse = 1000
		totalItems = 0

		try:
			quotaResponse = requests.get(quotaUrl, headers=headers)
			size = loads(quotaResponse.text)["limits"]["maxSearchResults"]
			url = "https://urlscan.io/api/v1/search/?q=domain:*.{0}&size={1}".format(domain, size)

			while itemsInResponse >= size:
				response = requests.get(url, headers=headers)
				jsonResponse = loads(response.text)

				if response.status_code != 200:
					print("  \__", colored(jsonResponse["message"], "red"))
					return US
				
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
				itemsInResponse = len(jsonResponse["results"])
				totalItems = int(jsonResponse["total"])

				if results:
					US.extend(results)
					US = list(set(US))
				
				if itemsInResponse > 0:
					lastItemString = "{0},{1}".format(jsonResponse["results"][-1]["sort"][0], jsonResponse["results"][-1]["sort"][1])
					url = "https://urlscan.io/api/v1/search/?q=domain:*.{0}&size={1}&search_after={2}".format(domain, size, lastItemString)
					sleep(2)

			US = set(US)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(US), "yellow")))
			return US

		except requests.exceptions.RequestException as err:
			print("  \__", colored(err, "red"))
			return US

		except requests.exceptions.HTTPError as errh:
			print("  \__", colored(errh, "red"))
			return US

		except requests.exceptions.ConnectionError as errc:
			print("  \__", colored(errc, "red"))
			return US

		except requests.exceptions.Timeout as errt:
			print("  \__", colored(errt, "red"))
			return US
		
		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return US