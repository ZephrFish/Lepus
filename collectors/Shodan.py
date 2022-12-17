import shodan
import requests
from re import findall
from json import dumps, loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	SD = []

	print(colored("[*]-Searching Shodan...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	SHODAN_API_KEY = parser.get("Shodan", "SHODAN_API_KEY")
	api = shodan.Shodan(SHODAN_API_KEY)

	if SHODAN_API_KEY == "":
		print("  \__", colored("No Shodan API key configured", "red"))
		return []

	else:
		try:
			response = requests.get("https://api.shodan.io/dns/domain/{0}?key={1}&history=True".format(domain, SHODAN_API_KEY))
			jsonResponse = loads(response.text)

			for subdomain in jsonResponse["subdomains"]:
				normalized="{0}.python.org".format(str(subdomain))
				SD.append(normalized)

			for res in api.search_cursor("hostname:.{0}".format(domain)):
				SD.extend([hostname for hostname in res["hostnames"] if ".{0}".format(domain) in hostname])

			for res in api.search_cursor("ssl:.{0}".format(domain)):
				SD.extend(findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), dumps(res)))

			SD = set(SD)

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

		except KeyError as errk:
			print("  \__", colored(errk, "red"))
			return SD

		except shodan.exception.APIError as err:
			print("  \__", colored(err, "red"))
			return SD

		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return SD
