import requests
from re import findall
from time import sleep
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	C = []

	print(colored("[*]-Searching Censys...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	API_URL = "https://search.censys.io/api/v2"
	maxPerPage = 100
	maxCensysPages = 20
	cursor = ""
	page = 1

	UID = parser.get("Censys", "CENSYS_UID")
	SECRET = parser.get("Censys", "CENSYS_SECRET")

	if UID == "" or SECRET == "":
		print("  \__", colored("No Censys API credentials configured", "red"))
		return []

	else:
		if not cursor:
			payload = {"q": domain, "per_page": maxPerPage}
		else: 
			payload = {"q": domain, "per_page": maxPerPage, "cursor": cursor}

		try:
			res = requests.post(API_URL + "/certificates/search", json=payload, auth=(UID, SECRET))

			if res.status_code == 403:
				print("  \__", colored("You have used your full quota for this billing period.", "red"))
				return C

			C = findall("CN=([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), str(res.content))
			nextCursor = findall("\{\"next\": \"(.*?)\"", str(res.content))

			while page <= maxCensysPages:
				sleep(3)
				payload = {"q": domain, "per_page": maxPerPage, "cursor": nextCursor[0]}
				res = requests.post(API_URL + "/certificates/search", json=payload, auth=(UID, SECRET))

				if res.status_code != 200:
					if loads(res.text)["error_type"] == "max_results":
						print("  \__", colored("Search result limit reached.", "red"))
						break

					elif loads(res.text)["error_type"] == "quota_exceeded":
						print("  \__", colored("Quota exceeded.", "red"))
						break

					elif loads(res.text)["error_type"] == "rate_limit_exceeded":
						print("  \__", colored("Rate-limit exceeded.", "red"))
						break
					
					elif res.status_code == 403 and "You have used your full quota for this billing period." in res.text:
						print("  \__", colored("You have used your full quota for this billing period.", "red"))
						break

					else:
						print("  \__ {0} {1} {2}".format(colored("An error occured on page", "red"), colored("{0}:".format(page), "red"), colored(loads(res.text)["error_type"], "red")))

				else:
					tempC = findall("CN=([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), str(res.content))
					nextCursor = findall("\{\"next\": \"(.*?)\"", str(res.content))
					C = C + tempC

				page += 1

			C = set(C)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(C), "yellow")))
			return C

		except KeyError as errk:
			print("  \__", colored(errk, "red"))
			return []

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
