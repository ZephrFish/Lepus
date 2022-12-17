import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	DNSR = []

	print(colored("[*]-Searching DNSRepo...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	DNSREPO_API_KEY = parser.get("DNSRepo", "DNSREPO_API_KEY")

	if DNSREPO_API_KEY == "":
		print("  \__", colored("No DNSRepo API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		url = "https://dnsrepo.noc.org/api/?apikey={0}&search={1}".format(DNSREPO_API_KEY, domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				DNSR.extend(results)
				DNSR = set(DNSR)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(DNSR), "yellow")))
			return DNSR

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