import requests
from re import findall
from termcolor import colored
from http.client import responses
from configparser import RawConfigParser


def init(domain):
	FH = []

	print(colored("[*]-Searching Fullhunt...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	FULLHUNT_API_KEY = parser.get("Fullhunt", "FULLHUNT_API_KEY")
	
	if FULLHUNT_API_KEY == "":
		print("  \__", colored("No Fullhunt API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-API-KEY": FULLHUNT_API_KEY}
		url = "https://fullhunt.io/api/v1/domain/{0}/subdomains".format(domain)

		try:
			response = requests.get(url, headers=headers)

			if response.status_code == 200:
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
				
				if results:
					FH.extend(results)
					FH = set(FH)
			
			else:
				print("  \__", colored("Response: {0} {1}".format(response.status_code, responses[response.status_code]), "red"))
				return []

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(FH), "yellow")))
			return FH

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