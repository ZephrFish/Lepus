from requests import get
from utilities.ScanHelpers import findSignatures


def myFindSignatures(domain, signatures, kati):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

	try:
		for signature in signatures:

			if signature in str(get("http://" + domain, headers=headers).history[0].content, "utf-8"):
				return True
			
			if signature in str(get("https://" + domain, headers=headers, verify=False).history[0].content, "utf-8"):
				return True

	except Exception:
		pass

	return False


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["to target URL: <a href=\"https://tictail.com"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "domains.tictail.com" in CNAME:
			if myFindSignatures(domain, signatures, 1):
				outcome = ["Tictail", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "46.137.181.142":
			if myFindSignatures(domain, signatures, 1):
				outcome = ["Tictail", domain, str(entry)]

	return outcome
