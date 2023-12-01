from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["<iframe src=\"//www.herokucdn.com/error-pages/no-such-app.html\">"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "herokuapp.com" in CNAME:
			if findSignatures(CNAME, signatures, 2):
				outcome = ["Heroku", domain, CNAME]

	return outcome
