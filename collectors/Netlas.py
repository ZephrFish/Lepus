import requests
from re import findall
from json import loads
from time import sleep
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	NL = []

	print(colored("[*]-Searching Netlas...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	NETLAS_API_KEY = parser.get("Netlas", "NETLAS_API_KEY")

	if NETLAS_API_KEY == "":
		print("  \__", colored("No Netlas API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Api-Key": NETLAS_API_KEY}
		profileUrl = "https://app.netlas.io/api/users/current/"
		url = "https://app.netlas.io/api/domains/download/"

		try:
			profileResponse = requests.get(profileUrl, headers=headers)
			maxDownloads = loads(profileResponse.text)["plan"]["limit_per_one_download"]
			params = {"q": "domain:(domain:*.{0} AND NOT domain:{1})".format(domain, domain), "fields": "domain", "size": int(maxDownloads), "source_type": "include"}

			response = requests.post(url, headers=headers, data=params)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				NL.extend(results)

			NL = set(NL)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(NL), "yellow")))
			return NL

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
