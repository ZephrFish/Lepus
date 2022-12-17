import requests
from json import loads
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	MV = []

	print(colored("[*]-Searching Maltiverse...", "yellow"))

	items = 500
	page = 0
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://api.maltiverse.com/search"

	try:
		while items == 500:
			params = {"query": "hostname.keyword:*.{0}".format(domain), "from": 500*page, "size": 500}
			response = requests.get(url, headers=headers, params=params)
			items = len(loads(response.text)["hits"]["hits"])
			page += 1

			if items > 0:
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
				MV.extend(results)

		MV = set(MV)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(MV), "yellow")))
		return MV

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
