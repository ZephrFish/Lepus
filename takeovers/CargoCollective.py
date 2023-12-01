from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["<title>404 &mdash; File not found</title>"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "cargocollective.com" in CNAME:
			if findSignatures(CNAME, signatures, 1):
				outcome = ["Cargo Collective", domain, CNAME]

	return outcome
