import requests
import datetime
from re import findall
from json import loads
from termcolor import colored


def init(domain):
	CC = []

	print(colored("[*]-Searching CommonCrawl...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	indexUrl = "https://index.commoncrawl.org/collinfo.json"
	currentYear = datetime.date.today().strftime("%Y")

	try:
		indexResponse = requests.get(indexUrl, headers=headers)
		items = loads(indexResponse.text)

		for aYear in range(int(currentYear)-1, int(currentYear)+1):
			for item in items:

				if str(aYear) in item["name"]:
					url = item["cdx-api"]
					params = {"url": "*.{0}".format(domain)}
					response = requests.get(url, headers=headers, params=params)
					results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
					
					if results:
						CC.extend(results)
		
		CC = set(CC)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(CC), "yellow")))
		return CC

	except requests.exceptions.RequestException as err:
		print("  \__", colored(err, "red"))
		return CC

	except requests.exceptions.HTTPError as errh:
		print("  \__", colored(errh, "red"))
		return CC

	except requests.exceptions.ConnectionError as errc:
		print("  \__", colored(errc, "red"))
		return CC

	except requests.exceptions.Timeout as errt:
		print("  \__", colored(errt, "red"))
		return CC
	
	except Exception:
		print("  \__", colored("Something went wrong!", "red"))
		return []
