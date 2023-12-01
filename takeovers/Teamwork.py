from requests import get
from warnings import simplefilter


simplefilter("ignore")


def init(domain, ARecords, CNAMERecords):
	outcome = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

	signatures = ["Unable to determine installationID from domain"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "teamwork.com" in CNAME:
			try:
				resp = get("https://{0}/launchpad/v1/info.json?suppressLoginModal=true&noErrorHandling=true".format(domain), headers=headers, verify=False)

				for signature in signatures:
					if signature in resp.text:
						outcome = ["Teamwork", domain, CNAME]
						return outcome

			except Exception as e:
				pass

	return outcome
