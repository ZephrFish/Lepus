import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	ROB = []

	print(colored("[*]-Searching Robtex...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	ROBTEX_API_KEY = parser.get("Robtex", "ROBTEX_API_KEY")

	if ROBTEX_API_KEY == "":
		url1 = "https://freeapi.robtex.com/pdns/forward/{0}".format(domain)
		url2 = "https://freeapi.robtex.com/pdns/reverse/{0}".format(domain)

	else:
		url1 = "https://proapi.robtex.com/pdns/forward/{0}?key={1}".format(domain, ROBTEX_API_KEY)
		url2 = "https://proapi.robtex.com/pdns/reverse/{0}?key={1}".format(domain, ROBTEX_API_KEY)

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	
	try:
		response1 = requests.get(url1, headers=headers)
		response2 = requests.get(url2, headers=headers)
		results1 = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response1.text)
		results2 = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response2.text)
		
		if results1:
			ROB.extend(results1)
			
		if results2:
			ROB.extend(results2)

		ROB = set(ROB)
		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(ROB), "yellow")))
		return ROB

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