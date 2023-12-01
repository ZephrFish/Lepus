from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["No settings were found for this company"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "helpscoutdocs.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Helpscout", domain, CNAME]

	return outcome
