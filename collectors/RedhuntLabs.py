import requests
from json import loads
from re import findall
from time import sleep
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	RHL = []

	print(colored("[*]-Searching Redhunt Labs...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	page = 1
	perPage = 1000
	maxPages = 3
	REDHUNTLABS_API_KEY = parser.get("RedhuntLabs", "REDHUNTLABS_API_KEY")

	if REDHUNTLABS_API_KEY == "":
		print("  \__", colored("No Redhunt Labs API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-BLOBR-KEY": REDHUNTLABS_API_KEY}
		url = "https://reconapi.redhuntlabs.com/community/v1/domains/subdomains"

		try:
			while page <= maxPages:
				RHL = list(RHL)
				params = {"domain": domain, "page": page, "page_size": perPage}

				response = requests.get(url, headers=headers, params=params)

				if response.status_code == 200:
					results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
					resultCount = loads(response.text)["metadata"]["result_count"]
					
					if resultCount % perPage > 0:
						maxPages = int(resultCount / perPage) + 1
					else:
						maxPages = int(resultCount / perPage)

					if results:
						RHL.extend([res.lower() for res in results])
						RHL = set(RHL)
					
					page += 1
					sleep(2)
				
				else:
					error_message = response.json()['message']

					if "limit has been reached" in error_message:
						print("  \__", colored("Your API credits have been exhausted.", "red"))
					
					return set(RHL)
			
			RHL = set(RHL)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(RHL), "yellow")))
			return RHL

		except requests.exceptions.RequestException as err:
			print("  \__", colored(err, "red"))
			return RHL

		except requests.exceptions.HTTPError as errh:
			print("  \__", colored(errh, "red"))
			return RHL

		except requests.exceptions.ConnectionError as errc:
			print("  \__", colored(errc, "red"))
			return RHL

		except requests.exceptions.Timeout as errt:
			print("  \__", colored(errt, "red"))
			return RHL
		
		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return RHL
