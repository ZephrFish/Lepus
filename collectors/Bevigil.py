import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	BEV = []

	print(colored("[*]-Searching Bevigil...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	BEVIGIL_API_KEY = parser.get("Bevigil", "BEVIGIL_API_KEY")

	if BEVIGIL_API_KEY == "":
		print("  \__", colored("No Bevigil API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Access-Token": BEVIGIL_API_KEY}
		url = "http://osint.bevigil.com/api/{0}/subdomains/".format(domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				BEV.extend(results)
				BEV = set(BEV)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(BEV), "yellow")))
			return BEV

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