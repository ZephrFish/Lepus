import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	FDB = []

	print(colored("[*]-Searching Farsight DNSDB...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	FARSIGHT_API_KEY = parser.get("FarsightDNSDB", "FARSIGHT_API_KEY")

	if FARSIGHT_API_KEY == "":
		print("  \__", colored("No Farsight DNSDB API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-API-KEY": FARSIGHT_API_KEY}
		url = "https://api.dnsdb.info/lookup/rrset/name/*.{0}?limit=1000000000000".format(domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				FDB.extend(results)
				FDB = set(FDB)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(FDB), "yellow")))
			return FDB

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