import requests
from re import findall
from termcolor import colored
from configparser import RawConfigParser


def init(domain):
	BO = []

	print(colored("[*]-Searching BufferOver...", "yellow"))

	parser = RawConfigParser()
	parser.read("config.ini")
	BUFFEROVER_API_KEY = parser.get("BufferOver", "BUFFEROVER_API_KEY")

	if BUFFEROVER_API_KEY == "":
		print("  \__", colored("No BufferOver API key configured", "red"))
		return []

	else:
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "X-Api-Key": BUFFEROVER_API_KEY}
		url = "https://tls.bufferover.run/dns?q=.{0}".format(domain)

		try:
			response = requests.get(url, headers=headers)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
			
			if results:
				BO.extend(results)
				BO = set(BO)

			print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(BO), "yellow")))
			return BO

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