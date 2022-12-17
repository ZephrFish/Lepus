import requests
from re import findall
from time import sleep
from json import loads
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	WS = []

	print(colored("[*]-Searching Webscout...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "content-type": "application/json"}
	url = "https://webscout.io/api/search/{0}".format(domain)

	try:
		creationResponse = requests.get(url, headers=headers)
		status = loads(creationResponse.text)["status"]

		if status == "created" or status == "running" or status == "success":
			creationID = loads(creationResponse.text)["id"]

			while status != "success":
				sleep(2)
				url = "https://webscout.io/api/search/status/{0}".format(creationID)
				runningResponse = requests.get(url, headers=headers)
				status = loads(runningResponse.text)["status"]

			url = "https://webscout.io/api/search/result/{0}".format(creationID)
			completedResponse = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), completedResponse.text)
			
			WS.extend(results)
			WS = set(WS)

		else:
			print("  \__", colored("Message: {0}".format(loads(creationResponse.text)["message"]), "red"))
			return WS
		

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(WS), "yellow")))
		return WS

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
