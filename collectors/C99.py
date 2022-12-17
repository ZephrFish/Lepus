import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	C99 = []

	print(colored("[*]-Searching C99...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	C99_API_KEY = parser.get("C99", "C99_API_KEY")

	if C99_API_KEY == "":
		print("  \__", colored("No C99 API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		url = "https://api.c99.nl/subdomainfinder?key={0}&domain={1}&json".format(C99_API_KEY, domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				C99.extend(results)
				C99 = set(C99)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(C99), "yellow")))
			return C99

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