import requests
from re import findall
from termcolor import colored


def init(domain):
	DNSD = []

	print(colored("[*]-Searching DNSDumpster...", "yellow"))

	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
	url = "https://dnsdumpster.com/"

	try:
		response = requests.get(url, headers=headers)
		csrfTokenRes = findall("<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"(.*)\">", response.text)
		cookieRes = response.cookies
		
		if csrfTokenRes and cookieRes:
			csrfToken = csrfTokenRes[0]
			cookie = cookieRes["csrftoken"]

			headers["Content-Type"] = "application/x-www-form-urlencoded"
			headers["Referer"] = "https://dnsdumpster.com"
			headers["X-CSRF-Token"] = csrfToken
			params = {"csrfmiddlewaretoken": csrfToken, "targetip": domain, "user": "free"}
			cookies = {"csrftoken" : cookie}

			response = requests.post(url, headers=headers, data=params, cookies=cookies)
			results = findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), response.text)
		
		else:
			print("  \__", colored("Could not retrieve CSRF token", "red"))
			return []
		
		if results:
			DNSD.extend(results)
			DNSD = set(DNSD)

		print("  \__ {0}: {1}".format(colored("Subdomains found", "cyan"), colored(len(DNSD), "yellow")))
		return DNSD

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
