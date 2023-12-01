from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Project doesnt exist... yet!"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "readme.io" in CNAME or "ssl.readmessl.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Readme.io", domain, CNAME]

	return outcome
