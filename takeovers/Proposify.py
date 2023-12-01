from requests import get
from warnings import simplefilter


simplefilter("ignore")


def init(domain, ARecords, CNAMERecords):
	outcome = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "ssl.proposify.com" in CNAME:
			try:
				response = get("https://{0}/domain".format(domain), headers=headers, verify=False)

				if "Why isn't my custom domain showing?" in response.text:
					outcome = ["Proposify", domain, CNAME]
					return outcome

			except Exception as e:
				print(e)

	return outcome
