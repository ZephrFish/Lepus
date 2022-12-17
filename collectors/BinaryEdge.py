import requests
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	BE = []

	print(colored("[*]-Searching BinaryEdge...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	BINARYEDGE_API_KEY = parser.get("BinaryEdge", "BINARYEDGE_API_KEY")

	if BINARYEDGE_API_KEY == "":
		print("  \__", colored("No BinaryEdge API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Key": BINARYEDGE_API_KEY}
		page = 1
		totalPages = 100

		try:
			while page < totalPages:
				url = "https://api.binaryedge.io/v2/query/domains/subdomain/{0}?page={1}".format(domain, page)
				response = requests.get(url, headers=headers)

				try:
					pageSize = loads(response.text)["pagesize"]
					total = loads(response.text)["total"]
					totalPages = total // pageSize

					if total % pageSize > 0:
						totalPages += totalPages

				except:
					print("  \__", colored("Json response error", "red"))
					return BE

				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
				page += 1

				if results:
					BE.extend(results)
			
			BE = set(BE)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(BE), "yellow")))
			return BE

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