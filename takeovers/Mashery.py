from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Unrecognized domain <strong>"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "mashery.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Mashery", domain, CNAME]

	return outcome
