from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Sorry, we could not find any content for this web address"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "acquia-test.co" in CNAME or "acquia-sites.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Acquia", domain, CNAME]

	return outcome
