import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	LIX = []

	print(colored("[*]-Searching LeakIX...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	LEAKIX_API_KEY = parser.get("LeakIX", "LEAKIX_API_KEY")

	if LEAKIX_API_KEY == "":
		print("  \__", colored("No LeakIX API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "Accept": "application/json", "Api-Key": LEAKIX_API_KEY}
		url = "https://leakix.net/api/graph/hostname/{0}?v%5B%5D=hostname&d=auto&l=1..5".format(domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				LIX.extend(results)
				LIX = set(LIX)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(LIX), "yellow")))
			return LIX

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