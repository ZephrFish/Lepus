import requests
from re import findall
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	HIO = []

	print(colored("[*]-Searching HunterIO...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	HUNTERIO_API_KEY = parser.get("HunterIO", "HUNTERIO_API_KEY")

	if HUNTERIO_API_KEY == "":
		print("  \__", colored("No HunterIO API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		url = "https://api.hunter.io/v2/domain-search"
		offset = 0
		limit = 100
		totalRuns = 100
		runCount = 0
		

		try:
			planUrl = "https://api.hunter.io/v2/account?api_key={0}".format(HUNTERIO_API_KEY)
			planResponse = requests.get(planUrl, headers=headers)
			planName = loads(planResponse.text)["data"]["plan_name"]
			
			if planName == "Free":
				limit = 10

			while runCount < totalRuns:
				params = {"domain": domain, "api_key": HUNTERIO_API_KEY, "limit": limit, "offset": offset}
				response = requests.get(url, headers=headers, params=params)
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
				totalResults = loads(response.text)["meta"]["results"]
				totalRuns = totalResults // limit

				if totalResults % limit > 0:
					totalRuns += 1
				
				if results:
					HIO.extend(results)
					HIO = list(set(HIO))

				if planName == "Free":
					runCount = totalRuns

				offset += 100
				runCount += 1				

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(HIO), "yellow")))
			return HIO

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