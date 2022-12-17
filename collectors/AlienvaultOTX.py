import requests
from re import findall
from termcolor import colored


def init(domain):
	OTX = []

	print(colored("[*]-Searching Alienvault OTX...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://otx.alienvault.com/api/v1/indicators/domain/{0}/passive_dns".format(domain)

	try:
		response = requests.get(url, headers=headers)
		results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
		
		if results:
			OTX.extend(results)
			OTX = set(OTX)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(OTX), "yellow")))
		return OTX

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
