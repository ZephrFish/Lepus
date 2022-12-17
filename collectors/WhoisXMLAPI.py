import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	WXA = []

	print(colored("[*]-Searching WhoisXML API...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	WHOISXML_API_KEY = parser.get("WhoisXMLAPI", "WHOISXML_API_KEY")

	if WHOISXML_API_KEY == "":
		print("  \__", colored("No WhoisXML API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		params = {"apiKey": WHOISXML_API_KEY, "domainName": domain}
		url = "https://subdomains.whoisxmlapi.com/api/v1"

		try:
			response = requests.get(url, headers=headers, params=params)

			if response.status_code == 402:
				print("  \__", colored("Insufficient API queries account balance.", "red"))
				return []
			
			if response.status_code == 429:
				print("  \__", colored("Too Many Requests. Try your call again later.", "red"))
				return []

			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				WXA.extend(results)
				WXA = set(WXA)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(WXA), "yellow")))
			return WXA

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