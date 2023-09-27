import base64
import requests
from json import loads
from re import findall
from time import sleep
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	QH = []

	print(colored("[*]-Searching Qianxin Hunter...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	page = 1
	perPage = 100
	maxPages = 3
	QIANXIN_API_KEY = parser.get("QianxinHunter", "QIANXIN_API_KEY")

	if QIANXIN_API_KEY == "":
		print("  \__", colored("No Qianxin Hunter API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
		url = "https://hunter.qianxin.com/openApi/search"
		search = "domain=\"{0}\"".format(domain)
		search = base64.b64encode(bytes(search, "utf-8")).decode("utf-8")

		try:
			while page <= maxPages:
				QH = list(QH)
				params = {"api-key": QIANXIN_API_KEY, "search": search, "page": page, "page_size": perPage, "is_web": 3}

				response = requests.get(url, headers=headers, params=params)
				results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)

				if loads(response.text)["code"] == 40204:
					print("  \__", colored("Quota exceeded!", "red"))
					break

				maxPages = int(loads(response.text)["data"]["total"] / perPage) + 1

				if results:
					QH.extend(results)
					QH = set(QH)
				
				page += 1
				sleep(2)
			
			QH = set(QH)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(QH), "yellow")))
			return QH

		except requests.exceptions.RequestException as err:
			print("  \__", colored(err, "red"))
			return QH

		except requests.exceptions.HTTPError as errh:
			print("  \__", colored(errh, "red"))
			return QH

		except requests.exceptions.ConnectionError as errc:
			print("  \__", colored(errc, "red"))
			return QH

		except requests.exceptions.Timeout as errt:
			print("  \__", colored(errt, "red"))
			return QH
		
		except Exception:
			print("  \__", colored("Something went wrong!", "red"))
			return QH