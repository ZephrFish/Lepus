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
	url = "https://api.webscout.io/lookup/{0}".format(domain)

	waitCounter = 0

	try:
		creationResponse = requests.get(url, headers=headers)
		status = loads(creationResponse.text)["status"]
		positionInQueue = loads(creationResponse.text)["queue_pos"]["pivot"]

		if status == "success": 
			found = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), creationResponse.text)
			WS.extend(found)
		elif status == "running": 
			found = []

		previousRunFound = -1

		if status == "running" or status == "success":
			while (positionInQueue != -1 or len(found) > previousRunFound) and waitCounter < 20:
				sleep(30)

				previousRunFound = len(found)
				runningResponse = requests.get(url, headers=headers)
				status = loads(runningResponse.text)["status"]
				positionInQueue = loads(runningResponse.text)["queue_pos"]["pivot"]

				if status == "success": 
					found = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), runningResponse.text)
					WS.extend(found)

				waitCounter += 1

		else:
			print("  \__", colored("Message: {0}".format(loads(creationResponse.text)["message"]), "red"))
			return WS

		WS = set(WS)

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
