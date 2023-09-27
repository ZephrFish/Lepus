import requests
from time import sleep
from re import findall
from termcolor import colored


def init(domain):
	DT = []

	print(colored("[*]-Searching Digitorus...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://certificatedetails.com/{0}".format(domain)

	try:
		response = requests.get(url, headers=headers)
		results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)

		if results:
			DT.extend(results)
			DT = list(set(DT))

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(DT), "yellow")))
		return DT

	except requests.exceptions.RequestException as err:
		print("  \__", colored(err, "red"))
		return DT

	except requests.exceptions.HTTPError as errh:
		print("  \__", colored(errh, "red"))
		return DT

	except requests.exceptions.ConnectionError as errc:
		print("  \__", colored(errc, "red"))
		return DT

	except requests.exceptions.Timeout as errt:
		print("  \__", colored(errt, "red"))
		return DT
	
	except Exception:
		print("  \__", colored("Something went wrong!", "red"))
		return DT
