import requests
from re import findall
from json import loads
from termcolor import colored


def init(domain):
	CE = []

	print(colored("[*]-Searching Columbus Elmasy...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://columbus.elmasy.com/api/lookup/{0}".format(domain)

	try:
		response = requests.get(url, headers=headers)
		results = [x for x in loads(response.text)]

		if results:
			CE.extend(results)
			CE = set(CE)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(CE), "yellow")))
		return CE

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
