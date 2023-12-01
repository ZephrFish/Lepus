from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["There's nothing here, yet.", "We could not find what you're looking for."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "helpjuice.com" in CNAME:
			if findSignatures(CNAME, signatures, 1):
				outcome = ["Helpjuice", domain, CNAME]

	return outcome
