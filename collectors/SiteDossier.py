import requests
from time import sleep
from re import findall
from termcolor import colored


def init(domain):
	SD = []

	print(colored("[*]-Searching Site Dossier...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "http://www.sitedossier.com/parentdomain/{0}".format(domain)

	try:
		response = requests.get(url, headers=headers)
		sites = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
		sites = list(set(sites))

		if sites:
			SD.extend(sites)

			for site in sites:
				url = "http://www.sitedossier.com/site/{0}".format(site)
				
				response = requests.get(url, headers=headers)
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)

				if results:
					SD.extend(results)
					SD = list(set(SD))
				
				sleep(2)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(SD), "yellow")))
		return SD

	except requests.exceptions.RequestException as err:
		print("  \__", colored(err, "red"))
		return SD

	except requests.exceptions.HTTPError as errh:
		print("  \__", colored(errh, "red"))
		return SD

	except requests.exceptions.ConnectionError as errc:
		print("  \__", colored(errc, "red"))
		return SD

	except requests.exceptions.Timeout as errt:
		print("  \__", colored(errt, "red"))
		return SD
	
	except Exception:
		print("  \__", colored("Something went wrong!", "red"))
		return SD
