import requests
from time import sleep
from json import loads
from re import findall
from termcolor import colored


def init(domain):
	RC = []

	print(colored("[*]-Searching Recon Cloud...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://recon.cloud/api/search?domain={0}".format(domain)
	step = "collect"
	leaveFlag = 0

	try:
		while step != "finished" and leaveFlag < 12:
			response = requests.get(url, headers=headers)
			step = loads(response.text)["step"]
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)

			if step == "filter":
				leaveFlag += 1

			if results:
				RC.extend(results)
				RC = list(set(RC))

			sleep(10)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(RC), "yellow")))
		return RC

	except requests.exceptions.RequestException as err:
		print("  \__", colored(err, "red"))
		return RC

	except requests.exceptions.HTTPError as errh:
		print("  \__", colored(errh, "red"))
		return RC

	except requests.exceptions.ConnectionError as errc:
		print("  \__", colored(errc, "red"))
		return RC

	except requests.exceptions.Timeout as errt:
		print("  \__", colored(errt, "red"))
		return RC

	except Exception:
		print("  \__", colored("Something went wrong!", "red"))
		return RC

#Depricated?
