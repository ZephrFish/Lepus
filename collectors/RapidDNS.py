import requests
from re import findall
from termcolor import colored


def init(domain):
	RDNS = []

	print(colored("[*]-Searching RapidDNS...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://rapiddns.io/subdomain/{0}?full=1".format(domain)

	try:
		response = requests.get(url, headers=headers)
		results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
		
		if results:
			RDNS.extend(results)
			RDNS = set(RDNS)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(RDNS), "yellow")))
		return RDNS

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
